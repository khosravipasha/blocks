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
parser.add_argument("-n", required = True, help = "number of perturbations per instance")

args = parser.parse_args()

n = int(args.n)

print("Making {} perturbations for each instance.".format(n))

#return

template_path = "in/devset_full_template.json"
instructions_path = "out/sample_purt.txt" # used for debugging
env_json_path = "out/env.json"


if __name__ == "__main__":
   
   
    # instructions = []
    # for i in range(n):
    #     instructions.append(indexed_string.get_sentence(result[i]))

    # # Writing pertubations to file
    # with open(instructions_path, "w") as f:
    #     for i in range(n):
    #         f.write(instructions[i])
    #         f.write("\n")


    # Filling out the template
    template = {}
    with open(template_path) as json_data:
        template = json.load(json_data)


        for instance in template:
            for note in instance['notes']:
                instruction = note['notes'][0]
                
                note['notes'] = []
                
              #  print(instruction)
                indexed_string = IndexedString(instruction, bow=False)
                result = purt.get_pertubations(indexed_string, n)

                note["masks"] = []

                for i in range(n):
                    note['notes'].append(indexed_string.get_sentence(result[i]))
                    note["masks"].append([int(x) for x in result[i]])


                note['users'] = ['dummy'] * n




        with open( env_json_path , "w") as jsonOut:
            json.dump(template, jsonOut)#, indent = 2)
