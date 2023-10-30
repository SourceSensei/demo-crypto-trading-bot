import logging
import requests
import pprint

logger = logging.getLogger()

# https://fapi.binance.com
# /fapi/v1/exchangeInfo

def get_contracts():
    response_object = requests.get("https://fapi.binance.com/fapi/v1/exchangeInfo")
    # print(response_object.status_code, response_object.json())
    # with pprint we manage to print the info in a nicer way
    # pprint.pprint(response_object.json())

    # pprint.pprint(response_object.json()['symbols'])

    contracts = []

    for contract in response_object.json()['symbols']:
        # pprint.pprint(contract)
        # print(contract['pair'])
        contracts.append(contract['pair'])

    return contracts

print(get_contracts())