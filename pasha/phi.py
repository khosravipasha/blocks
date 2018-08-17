import json
import pickle
import os
import sys
import numpy as np
import sys

from collections import Counter

from lime.lime_text import LimeTextExplainer
from phis import *

def choose_phi(name):
    return {
        'phi_changed': phi_changed,
        'phi_percent_changed': phi_percent_changed,
        'phi_block_moved': phi_block_moved,
        'phi_stop': phi_stop,
        'phi_num_moves': phi_num_moves,
        'phi_comp_distance': phi_comp_distance,
        'phi_len': phi_len,
        'phi_constant': phi_constant,
        'phi_random': phi_random,
        "phi_destination": phi_destination
    }.get(name, phi_changed)

phi = choose_phi(sys.argv[1])

###############################
# Writing phi values to instruction_to_actions.json for each action

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

    with open(instruction_to_actions, "w") as actionJsonWrite:
        json.dump(actions, actionJsonWrite, indent = 2)

############################################
# Uses generated Phi values and LIME to generate a explanation
#
import sys
sys.path.insert(0, '/home/pasha/ML/lime/lime')
from lime_text import LimeTextExplainer

data = pickle.load( open(matrix_pickle_file, "rb" ) )

print(data.shape)
actionsJson = json.load( open(instruction_to_actions, "r") )

class_names=["Class 0", "Class 1"]
explainer = LimeTextExplainer(class_names=class_names)

def classifier_fn(texts):
    d = len(texts)
    k = 2
    ans = np.zeros( (d, k) )

    for ind, txt in enumerate(texts):
        PHI = actionsJson["perturbs"][txt]["phi"]
        print (PHI, txt)
        for j in range(len(PHI)):
            ans[ind][j] = PHI[j]
    return ans

exp = explainer.explain_json_instance(actions["original"], classifier_fn, data=data)
exp.save_to_file('out/explain.html')
