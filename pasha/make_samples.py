'''

This is for generating purturbation of text using LIME's funciton

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

def get_pertubations(indexed_string,
                                num_samples,
                                distance_metric = 'cosine'):
        """
        Generates neighborhood data by randomly removing words from
        the instance. At most removes 2/3 of the text.

        Args:
            indexed_string: document (IndexedString) to be explained,
            num_samples: size of the neighborhood to learn the linear model
            distance_metric: the distance metric to use for sample weighting,
                defaults to cosine similarity
        Returns:
                data: dense num_samples * K binary matrix, where K is the
                    number of tokens in indexed_string. The first row is the
                    original instance, and thus a row of ones.

        """
        doc_size = indexed_string.num_words()
        sample = np.random.randint(1, 2 * doc_size / 3, num_samples - 1)
        data = np.ones((num_samples, doc_size))
        data[0] = np.ones(doc_size)
        features_range = range(doc_size)
        inverse_data = [indexed_string.raw_string()]
        for i, size in enumerate(sample, start=1):
            inactive = np.random.choice(features_range, size, replace=False)
            data[i, inactive] = 0
            inverse_data.append(indexed_string.inverse_removing(inactive))

        return data

#########################################################
##


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

# TODO
# 1. Save pickle options

if __name__ == "__main__":
    indexed_string = IndexedString(instruction, bow=False)
    result = get_pertubations(indexed_string, n)

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
