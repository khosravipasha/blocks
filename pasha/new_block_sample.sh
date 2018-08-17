# Makes a new sample and replaces the requred filed

# "Put block 9 in the first open space above block 11."
# "Take block number 9 and place it above block number 10."

# "Pick block number 9 and place it above block number 1"

# Put block 3 in the first open space to the right of block 16.

# python make_samples.py -n 160 -ins "Put block 5 in the first open space to the right of block 11"
python src/purturbe_env.py -n 300 -ins "Put block 5 in the first open space to the right of block 11"

echo "Copying env.json to simulator's json file"
cp out/env.json ../BlockWorldSimulator/Assets/devset.json

# TODO Change Agent's run cound in constants.py

if [ -z "$1" ]; then
  echo "no copy";
else
  echo "Copying to $1";
  mkdir -p ./out/save/$1;
  cp out/env.json ./out/save/$1/; 
fi


echo "DONE"
