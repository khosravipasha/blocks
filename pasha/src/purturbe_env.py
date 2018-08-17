import numpy as np
from collections import defaultdict
from functools import partial
import argparse
import pickle
import json
import copy

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

    instruction = " ".join( map(str, range(0,blocks)) )

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

        originalEnv = copy.deepcopy(template[0])
        
        template.pop()

        originalStart = np.copy(originalEnv['states'][0])
        originalEnd = np.copy(originalEnv['states'][1])
        originalImages = np.copy(originalEnv['images'])

        moved_block = None
        diff = np.mean(originalEnd != originalStart, axis=1)
        for i in range(len(diff)):
            if diff[i] > 0:
                moved_block = i+1
                break

        print("Moved block was {}".format(moved_block))


        originalEnv['states']= []
        originalEnv['notes'] = []
        originalEnv['images'] = []
        
        uniq_state_count = 0
        for index, block_remain in enumerate(keep_blocks):
            currentEnv = copy.deepcopy(originalEnv)            
            uniq_state_count += 1

            keep = set(map(int,block_remain.split(" ")))
            keep.add(moved_block)
            newStart = []
            newEnd   = []

            # Adding all states
            removed = 0
            for b in range(0, blocks):
                if b in keep:
                    newStart.append(list(originalStart[b]))
                    newEnd.append(list(originalEnd[b]))
                    #currentEnv['images'].append(originalImages[b])
                else:
                    ##### Random placement, and not cloder than a threshold
                    # okay = False
                    # while not okay:
                    #     x = 2 * np.random.rand() - 1
                    #     y = 2 * np.random.rand() - 1


                    #     curStart = [x, 0.1, y]
                    #     curEnd   = [y, 0.1, y]

                    #     okay = True
                    #     for z in range(len(newStart)):
                    #         dist = np.linalg.norm( np.array(newStart[z]) - np.array(curStart) )
                    #         if dist < 0.35:
                    #             okay = False
                    #             break         


                    # ###### move alittle bit around
                    # curStart = list(originalStart[b])
                    # curEnd   = list(originalEnd[b])
                    # curStart[0] += 5
                    # curStart[2] += 5
                    # curEnd[0] += 5
                    # curEnd[2] += 5

                    #continue
                    ####### OUTside
                    removed += 1
                    # #outside = [+2 + removed * 0.2, 0.1, 2 + removed * 0.2]
                    outside = [-1 + removed * 0.2, 0.1, -1]
                    curStart = list(outside)
                    curEnd = list(outside)
                    


                    # adding to the list
                    newStart.append(list(curStart))
                    newEnd.append(list(curEnd))
                    
                  
            assert(len(newStart) == len(newEnd))

            currentEnv['states'].append(list(newStart))
            currentEnv['states'].append(list(newEnd))

            cur_note = dict()
            cur_note["start"] = 0 #2*(uniq_state_count-1)
            cur_note["finish"] = 1 #2*(uniq_state_count-1)+1
            cur_note["type"] = "A0"
            cur_note["users"] = list(["dummy"])
            cur_note["notes"] = list([string_instruction])

            cur_note['debug'] = block_remain

            currentEnv['notes'].append(cur_note)
            #currentEnv["images"] = originalEnv["images"]
            template.append(currentEnv)


    # dump environment
    with open( env_json_path , "w") as jsonOut:
        json.dump(template, jsonOut, indent = 2)
