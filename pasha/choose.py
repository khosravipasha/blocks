import sys
import json
# sample run

# python choose.py instance_name phi_name

instance = sys.argv[1]
phi_name = sys.argv[2]

template_path = "in/choose_template.html"
env_json_path = "out/save/" + instance + "/env.json"
ins2action_path = "out/instruction_to_actions.json"

out_path = "out/choose.html"


env_json = open(env_json_path, 'r').read()
ins2action = open(ins2action_path, 'r').read()


env = json.dumps(json.loads(env_json))
ins = json.dumps(json.loads(ins2action))



template = open(template_path, 'r').read()

template = template.replace("REPLACE_FOR_ENV", env)
template = template.replace("REPLACE_FOR_JSON", ins)

open(out_path, "w").write(template)



