# Makes a new sample
# for each instance 
#   1. it chooses the first instrction
#   2. purturbes the first instruciton n times


python make_global_sample.py -n 50

echo "Copying env.json to simulator's json file"
cp out/env.json ../BlockWorldSimulator/Assets/devset.json

if [ -z "$1" ]; then
  echo "Warning: no copy to ./out/save";
else
  echo "Copying to $1";
  mkdir -p ./out/save/$1;
  cp out/env.json ./out/save/$1/;
fi

echo "DONE"
