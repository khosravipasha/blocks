# import json
#
# # somethings are hardcoded will need to automate it more
#
# template_path = "devset_template.json"
# instructions_path = "sample_purt.txt"
#
# # Reading instructions file line by line
# instructions = []
# with open(instructions_path) as text:
#     for l in text:
#         instructions.append(l)
#
#
# # Filling out the template
# template = {}
# with open(template_path) as json_data:
#     template = json.load(json_data)
#
#     for ins in instructions:
#         template[0]['notes'][0]['notes'].append(ins.strip())
#         template[0]['notes'][0]['users'].append("dummy")
#
#
# print(json.dumps(template, indent = 2))
