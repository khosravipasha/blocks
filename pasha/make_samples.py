'''

This is for generating purturbation of text using LIME's funciton
writes files to ./out/ folder and reads from ./in/

'''
from __future__ import unicode_literals

import sys
import itertools
import re

import numpy as np
import scipy as sp
import sklearn

import pickle
import json

import argparse

import sys
sys.path.insert(0, '/home/pasha/ML/lime/lime')
from lime_text import IndexedString

from src import lime_purturbation as purt


parser = argparse.ArgumentParser()
parser.add_argument("-n", required = True, help = "number of perturbations")
parser.add_argument("-ins", required = True, help = "original instruction")

args = parser.parse_args()

n = int(args.n)
instruction = args.ins #  "Put block 9 in the first open space above block 11."

print("Making {} perturbations for:".format(n))
print("\t{}".format(instruction))

#return

template_path = "in/devset_template.json"
instructions_path = "out/sample_purt.txt"
pert_matrix_path = "out/pert_matrix.p"
env_json_path = "out/env.json"


if __name__ == "__main__":
    indexed_string = IndexedString(instruction, bow=False)
    result = purt.get_pertubations(indexed_string, n)

    # making instruction pertubations
    instructions = []
    for i in range(n):
        instructions.append(indexed_string.get_sentence(result[i]))

    # Writing pertubations to file
    with open(instructions_path, "w") as f:
        for i in range(n):
            f.write(instructions[i])
            f.write("\n")

    pickle.dump( result, open( pert_matrix_path, "wb" ) )

    # Filling out the template
    template = {}
    with open(template_path) as json_data:
        template = json.load(json_data)

        for ins in instructions:
            template[0]['notes'][0]['notes'].append(ins.strip())
            template[0]['notes'][0]['users'].append("dummy")

    with open( env_json_path , "w") as jsonOut:
        json.dump(template, jsonOut, indent = 2)
