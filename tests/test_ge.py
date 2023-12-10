# test that the ge Class works as expected

from osrs_gear_price import GrandExchange

def test_grand_exchange():
    ge = GrandExchange()
    item_data = ge.get_item(4151) # get the item with id 4151 (Abyssal whip)
    print(item_data)
    #assert True == False