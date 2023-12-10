import json


# create json pretty printer function
def json_pprint(json_data):
    print(json.dumps(json_data, indent=4, sort_keys=True))


def format_number(number: int | float) -> str:
    """
    Formats a number to have commas at thousands, millions, etc
    """
    if not number:
        return "0"
    return "{:,}".format(number)
