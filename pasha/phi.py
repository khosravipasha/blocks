import json
import pickle
import os
import sys
import numpy as np

from collections import Counter

from lime.lime_text import LimeTextExplainer

##############################
# phi returns a number between 0 and 1 based on
# the actions for originalActions
def phi_changed(newActions, originalActions):
    if(len(newActions) != len(originalActions)):
        return [1,0]

    for i in range(len(newActions)):
        if newActions[i] != originalActions[i]:
            return [1,0]

    return [0,1]


def phi_percent_changed(newActions, originalActions):

    newSet = Counter(newActions)
    originalSet = Counter(originalActions)

    intersect = newSet & originalSet

    same = 0.0
    for uniq in intersect:
        same += intersect[uniq] * 2


    ans = same / (len(newActions) + len(originalActions))
    return [1 - ans , ans]

phi = phi_percent_changed

###############################

instruction_to_actions = "out/instruction_to_actions.json"
matrix_pickle_file = "out/pert_matrix.p"

with open(instruction_to_actions, "r") as actionJson:
    actions = json.load(actionJson)
    original = actions["original"]
    originalActions = actions["perturbs"][original]["actions"]
    actions["originalActions"] = originalActions

    for l in actions["perturbs"]:
        thisActions = actions["perturbs"][l]["actions"]
        currentPhi =  phi(thisActions, originalActions)
        actions["perturbs"][l]["phi"] = currentPhi

        # for debugging TODO remove
        print("~", currentPhi, l)

    with open(instruction_to_actions, "w") as actionJsonWrite:
        json.dump(actions, actionJsonWrite, indent = 2)


############################################

import sys
sys.path.insert(0, '/home/pasha/ML/lime/lime')
from lime_text import LimeTextExplainer

data = pickle.load( open(matrix_pickle_file, "rb" ) )
actionsJson = json.load( open(instruction_to_actions, "r") )

class_names=["Changed", "Not Changed"]
explainer = LimeTextExplainer(class_names=class_names)

def classifier_fn(texts):
    d = len(texts)
    k = 2
    ans = np.zeros( (d, k) )

    for ind, txt in enumerate(texts):
        PHI = actionsJson["perturbs"][txt]["phi"]
        print("!" , txt, PHI)
        for j in range(len(PHI)):
            ans[ind][j] = PHI[j]
    return ans

exp = explainer.explain_json_instance(actions["original"], classifier_fn, data=data)
exp.save_to_file('out/explain.html')
