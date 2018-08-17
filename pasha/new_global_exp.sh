# Uses the last round of output form simulation to generate an explanation


echo "Copying simulations results"

N=50
TOTAL=500

cp ../BlockWorldRoboticAgent/instruction_to_actions.json out/instruction_to_actions.json

declare -a arr=(
  "phi_changed"
  "phi_percent_changed"
  "phi_block_moved"
  "phi_stop"
  "phi_len"
  "phi_num_moves"
  "phi_constant"
  "phi_comp_distance"
  "phi_random"
  "phi_destination"
)

for i in "${arr[@]}"
do
  python phi_global.py -phi $i -n $N -total $TOTAL > out/save/$1/global_$i.txt

  if [ -z "$1" ]; then
    echo "Results not copied anywhere, temporarily saved in ./out folder";
  else
    echo "Copying results to ./out/save/$1";
    mkdir -p ./out/save/$1;
    cp  out/instruction_to_actions.json ./out/save/$1/instruction_to_actions.json;
  fi

done
