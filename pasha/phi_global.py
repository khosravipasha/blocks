import json
import pickle
import os
import sys
import numpy as np
import sys

import argparse

from collections import Counter
from collections import defaultdict

#from lime.lime_text import LimeTextExplainer
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


THRESHOLD = 0.5

parser = argparse.ArgumentParser()
parser.add_argument("-n", required = True, help = "number of perturbations per instance")
parser.add_argument("-total", required = True, help = "Total number ran (in case not everything is ran in env.json")
parser.add_argument("-phi", required = True, help = "which phi function")

args = parser.parse_args()

n = int(args.n)
phi = choose_phi(args.phi)
total = int(args.total)
###############################
# Writing phi values to instruction_to_actions.json for each action
#

instruction_to_actions = "out/instruction_to_actions.json"
env_json_file = "out/env.json"

with open(instruction_to_actions, "r") as actionJson:
    actions = json.load(actionJson)
    

    phi_forIndexed = []
    for i, curActions in enumerate(actions["indexed"]):
        
        # This is the original for current batch
        if i % n == 0:
            originalActions = actions["indexed"][i] 
            currentPhi = [0,1]
        else:
            currentPhi =  phi(curActions, originalActions)

        phi_forIndexed.append(currentPhi)
    
    actions["indexed_phi"] = phi_forIndexed


    ################ Analysis ###############

    remove_count = defaultdict(int)
    change_count = defaultdict(int)

    with open(env_json_file, "r") as env_json:
        
        env_all = json.load(env_json)
        index  = 0

        for _i, env in enumerate(env_all):
            if index >= total:
                break            

            for _j, note in enumerate(env["notes"]):
                if index >= total:
                    break
            
                originalInstructionWordsList = note["notes"][0].split(" ")

                for z in range(n):

                    currentActionMask = note["masks"][z]

            
                    removed_words = []
                    for i in range(len(currentActionMask)):
                        if currentActionMask[i] == 0:
                            removed_words.append(originalInstructionWordsList[i])

                    cur_phi = actions["indexed_phi"][index][0]
                    index += 1
    
                    for word in removed_words:
                        remove_count[word] += 1
                        if cur_phi > THRESHOLD:
                            change_count[word] += 1


        print("{} \t {} \t {}".format("word", "# changed phi", "# word removed"))
        results = []
        for z in change_count.keys():
            results.append( ( (1.0*change_count[z]) / remove_count[z], z) )
            #print("{} \t {} \t {}".format(z, change_count[z], remove_count[z]))

        results = sorted(results)
        for r in results:
            z = r[1]
            print("{}\t\t{}\t\t{}\t\t{}".format(z, 
                        change_count[z], 
                        remove_count[z],
                        1.0*change_count[z]/remove_count[z]
                        )
                )
