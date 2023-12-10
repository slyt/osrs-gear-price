# Creates a dataframe of all items in OSRS and their prices
# and saves to a pickle for post-processing
import logging

import pandas as pd
from osrsbox import items_api

from osrs_gear_price.ge import GrandExchange
from osrs_gear_price.util import format_number

# from osrs_gear_price.util import json_pprint


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
logger.propagate = True

ge = GrandExchange()
items = items_api.load()  # Load all items into memory

row_list = []  # create list of dicts to convert to dataframe later
exception_count = 0

for item in items:
    # if item.name != "Abyssal whip":
    #     # Skip to the next item
    #     continue
    if not item.equipable_by_player:
        continue
    if "Last Man Standing" in item.wiki_name:
        continue
    if not item.tradeable_on_ge:
        continue

    item.icon

    try:
        # Get the item price
        item_prices = ge.get_item(item.id)
        avgHighPrice = item_prices["avgHighPrice"]
        avgHighPrice = format_number(avgHighPrice)
        print(f"{item.name} ({item.id})-------{avgHighPrice}")
        equipment_stats_dict = item.equipment.construct_json()
        row_list.append(
            {
                "name": item.name,
                "id": item.id,
                **item_prices,
                **equipment_stats_dict,
                "icon": item.icon,
            }
        )
    except ValueError as e:
        exception_count += 1
        logger.debug(f"Could not get item price for {item.name} (id: {item.id}): {e}")

    # json_pprint(equipment_stats_dict)
    # exit()
    # json_pprint(item.construct_json())
print(f"Exception count: {exception_count}")

# Create dataframe from row_list
df = pd.DataFrame(row_list)
# Sort by avgHighPrice
df = df.sort_values(by=["avgHighPrice"], ascending=False)
# print top 10
print(df.head(10))
print(df.columns)


# Save dataframe to pickle file
df.to_pickle("data/dataframe.pkl")
