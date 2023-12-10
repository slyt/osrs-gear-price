import json
import logging
import time
from typing import TypedDict

import requests


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class ItemPrices(TypedDict):
    avgHighPrice: int
    highPriceVolume: int
    avgLowPrice: int
    lowPriceVolume: int


class GrandExchange:
    """
    Class for retrieving and caching price data from
    the OSRS wiki Grand Exchange API
    """

    def __init__(self):
        self.user_agent = "price_plotting - @sir.nibbler"
        self.url_1h = "https://prices.runescape.wiki/api/v1/osrs/1h"
        self.url_latest = "https://prices.runescape.wiki/api/v1/osrs/latest"

        self.last_request_time = 0
        self.cache_time = 3600  # 1 hour in seconds
        self.cache = {}  # contains entries like {item_id: {"price_high": 123}}
        self.cache_miss = 0
        self.cache_hit = 0
        self.cache_refresh = 0

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
            self.cache_refresh += 1

        if str(item_id) in self.cache:
            item_prices: ItemPrices = self.cache[str(item_id)]
            self.cache_hit += 1
            return item_prices
        else:
            logger.debug(f"Item ID {item_id} not found in cache")
            self.cache_miss += 1
            raise ValueError(
                f"Item ID {item_id} not found in cache. It is probably not frequently traded on the GE"
            )

    def update_cache(self):
        headers = {"User-Agent": self.user_agent}
        try:
            response = requests.get(self.url_1h, headers=headers)
            response.raise_for_status()
            self.last_request_time = time.time()
            self.cache = response.json()["data"]
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            logger.error(f"While fetching data {response.url}, got error: {e}")
            return
