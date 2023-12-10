import json
import logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

from osrsbox import items_api
import pandas as pd
import requests


from osrs_gear_price.util import json_pprint
from osrs_gear_price import GrandExchange

ge = ge.GrandExchange()


items = items_api.load() # Load all items into memory

row_list = [] # create list of dicts to convert to dataframe later

exception_count = 0

# Get all items with the name "Abyssal whip"
for item in items:
    # if item.name != "Abyssal whip":
    #     # Skip to the next item
    #     continue
    if item.equipable_by_player == False:
        continue
    if "Last Man Standing" in item.wiki_name:
        continue
    if item.tradeable_on_ge == False:
        continue

    try:
        # Get the item price
        item_prices = ge.get_item(item.id)
        avgHighPrice = item_prices["avgHighPrice"]
        # format avgHighPrice to have commas at thousands, millions, etc
        avgHighPrice = "{:,}".format(avgHighPrice)
        print(f"{item.name}-------{avgHighPrice}")
        equipment_stats_dict = item.equipment.construct_json()
        row_list.append({"name": item.name, "id": item.id, **item_prices, **equipment_stats_dict})
    except:
        exception_count += 1
        logger.debug(f"Warning: Item ID {item.id} {item.name} not found in cache. It is probably not frequently traded on the GE.")
        
    #json_pprint(equipment_stats_dict)
    #exit()
    #json_pprint(item.construct_json())
print(f"Exception count: {exception_count}")

# Create dataframe from row_list
df = pd.DataFrame(row_list)
# Sort by avgHighPrice
df = df.sort_values(by=["avgHighPrice"], ascending=False)
# print top 10
print(df.head(10))
print(df.columns)

# TODO: Calculate the price per stat for each item
# TODO: Plot price per stat for the highest stats for each stat category

