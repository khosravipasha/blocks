# Uses the last round of output form simulation to generate an explanation


echo "Copying simulations results"

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
  python phi.py $i
  python choose.py $1 $i

  if [ -z "$1" ]; then
    echo "only saving in out/explain.html";
  else
    echo "Copying to $1";
    mkdir ./out/save/$1;
    mv ./out/explain.html ./out/save/$1/explain_$1_$i.html;
    cp ./out/instruction_to_actions.json ./out/save/$1;
    cp ./out/choose.html ./out/save/$1/choose_$1_$i.html;
  fi

done
