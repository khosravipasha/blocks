import json
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-f", required = True, help = "json file path")

args = parser.parse_args()
fileName = args.f

with open(fileName, "r") as json_file:
    content = json_file.read()


parsed = json.loads(content)
print(json.dumps(parsed, indent=2, sort_keys=True))
