# Makes a new sample and replaces the requred filed

python make_samples.py -n 50 -ins "Put block 9 in the first open space above block 11."


echo "Copying env.json to simulator's json file"
cp out/env.json ../BlockWorldSimulator/Assets/devset.json

# TODO Change Agent's run cound in constants.py


echo "DONE"
