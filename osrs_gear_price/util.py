import json


# create json pretty printer function
def json_pprint(json_data):
    print(json.dumps(json_data, indent=4, sort_keys=True))
