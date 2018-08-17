import numpy as np
from collections import defaultdict
from functools import partial
import argparse
import pickle
import json

from src import lime_purturbation as purt
import sys
sys.path.insert(0, '/home/pasha/ML/lime/lime')
from lime_text import IndexedString

template_path = "in/devset_template.json"
keep_blocks_path = "out/sample_purt.txt" # "out/keep_blocks.txt"
pert_matrix_path = "out/pert_matrix.p" #"out/pert_matrix_blocks.p"
env_json_path = "out/env.json"
blocks = 20

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", required = True, help = "number of perturbations")
    parser.add_argument("-ins", required = True, help = "original instruction")

    args = parser.parse_args()
    n = int(args.n)
    string_instruction = args.ins

    instruction = " ".join( map(str, range(1,blocks + 1)) )

    print("Making {} perturbed envs".format(n))
    print(string_instruction)
    print(instruction)

    indexed_string = IndexedString(instruction, bow=False)
    result = purt.get_pertubations(indexed_string, n)


    keep_blocks = []
    for i in range(n):
        keep_blocks.append(indexed_string.get_sentence(result[i]))


    with open(keep_blocks_path, "w") as f:
        for i in range(n):
            f.write(keep_blocks[i])
            f.write("\n")
    pickle.dump( result, open( pert_matrix_path, "wb" ) )


    # make the environments
    with open(template_path) as json_data:
        template = json.load(json_data)

        originalStart = np.copy(template[0]['states'][0])
        originalEnd = np.copy(template[0]['states'][1])


        # the moved_block should not be removed 
        # otherwise the whole simluation stops working

        moved_block = None
        diff = np.mean(originalEnd != originalStart, axis=1)
        for i in range(len(diff)):
            if diff[i] > 0:
                moved_block = i+1
                break


        template[0]['states'].pop()
        template[0]['states'].pop()
        template[0]['notes'].pop()
        
        uniq_state_count = 0
        stateSet = set()

        for index, block_remain in enumerate(keep_blocks):
            if block_remain in stateSet:
                continue
            
            uniq_state_count += 1

            keep = set( map(int,block_remain.split(" ")))
            keep.add(moved_block) #always have moved_block
            newStart = []
            newEnd   = []

            # Adding all states
            for b in range(1, blocks+1):
                removed = 0
                if b in keep:
                    newStart.append(list(originalStart[b-1]))
                    newEnd.append(list(originalEnd[b-1]))
                else:
                    removed += 1
                    outside = [-0.2*removed, 0.1, -1.5]
                    newStart.append(list(outside))
                    newEnd.append(list(outside))

            assert(len(newStart) == len(newEnd))
            template[0]['states'].append(list(newStart))
            template[0]['states'].append(list(newEnd))

            cur_note = dict()
            cur_note["start"] = 2*(uniq_state_count-1)
            cur_note["finish"] = 2*(uniq_state_count-1)+1
            cur_note["type"] = "A0"
            cur_note["users"] = list(["dummy"])
            cur_note["notes"] = list([string_instruction])


            template[0]['notes'].append(cur_note)


    # dump environment
    with open( env_json_path , "w") as jsonOut:
        json.dump(template, jsonOut, indent = 2)
