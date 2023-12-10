# test that the ge Class works as expected
from osrs_gear_price import GrandExchange

ABYSSAL_WHIP_ID = 4151


def test_ge_init():
    ge = GrandExchange()
    assert ge.cache == {}


def test_ge_get_item():
    ge = GrandExchange()  # 4151 is the item ID for Abyssal whip
    assert ge.get_item(ABYSSAL_WHIP_ID) != {}


def test_ge_request_time():
    ge = GrandExchange()
    first_request_time = ge.last_request_time
    ge.update_cache()
    second_request_time = ge.last_request_time
    assert second_request_time > first_request_time


def test_ge_cache_refresh():
    ge = GrandExchange()
    ge.get_item(ABYSSAL_WHIP_ID)
    assert ge.cache_refresh == 1


def test_ge_cache_hit():
    ge = GrandExchange()
    ge.get_item(ABYSSAL_WHIP_ID)  # cache refresh + hit
    ge.get_item(ABYSSAL_WHIP_ID)  # cache hit
    assert ge.cache_hit == 2
