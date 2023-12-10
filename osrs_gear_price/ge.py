# create a class called GrandExchange that will request all of the data from the osrs wiki Grand Exchange API
# It will have a function called get_price(item_id) that will return the current price of the item
# It will cache the data for an hour. If an hour has passed, it will request the data again if get_price is called

import requests
import time
import logging
from util import json_pprint
from typing import TypedDict
from typing import Union

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class ItemPrices(TypedDict):
    avgHighPrice: int
    highPriceVolume: int
    avgLowPrice: int
    lowPriceVolume: int

class GrandExchange:
    def __init__(self):
        self.user_agent = "price_plotting - @sir.nibbler"
        self.url_1h = "https://prices.runescape.wiki/api/v1/osrs/1h"
        self.url_latest = "https://prices.runescape.wiki/api/v1/osrs/latest"

        self.last_request_time = 0
        self.cache_time = 3600 # 1 hour in seconds
        self.cache = {} # contains entries like {item_id: {"price_high": 123}
    
    def get_item(self, item_id: int | str) -> ItemPrices:
        """
        Returns an ItemPrices object for the given item_id

        Example retur value for item_id 4151 (Abyssal whip):
        {
            "avgHighPrice": 60242,
            "avgLowPrice": 59555,
            "highPriceVolume": 99,
            "lowPriceVolume": 155
        }
        """
        # check if we need to update the cache based on self.cache_time
        if time.time() - self.last_request_time > self.cache_time:
            self.update_cache()
            logger.debug("Updating cache")

        if str(item_id) in self.cache:
            item_prices: ItemPrices = self.cache[str(item_id)]
            #json_pprint(item_prices)
            return item_prices
        else:
            logger.debug(f"Item ID {item_id} not found in cache")
            return None
    def update_cache(self):
        headers = {'User-Agent': self.user_agent}
        try:
            response = requests.get(self.url_1h, headers=headers)
            response.raise_for_status()
            # set last request time
            self.last_request_time = time.time()
            self.cache = response.json()["data"]
            #json_pprint(self.cache)
        except:
            logger.error(f"ERROR: Got non-200 status code {response.status_code} from {response.url}")
            return