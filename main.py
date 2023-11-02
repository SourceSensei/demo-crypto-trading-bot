import tkinter as tk
import logging
from connectors.binance_futures import BinanceFuturesClient
from connectors.bitmex import BitmexClient

logger = logging.getLogger()

logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('info.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

# logger.debug("This message is important only when debugging the program")
# logger.info("This message just shows basic information")
# logger.warning("This message is about something you should pay attention to")
# logger.error("This message helps to debug an error that occurred in your program")

if __name__ == '__main__':
    binance = BinanceFuturesClient("PUBLIC_KEY",
                                   "PRIVATE_KEY", True)
    # print(binance.get_contracts())
    # print(binance.get_bid_ask("BTCUSDT"))
    # print(binance.get_balances())
    # print(binance.place_order("BTCUSDT", "BUY", 0.01, "LIMIT", 20000, "GTC"))
    # print(binance.get_order_status("BTCUSDT", 3503600231))
    # print(binance.cancel_order("BTCUSDT", 3503600231))

    bitmex = BitmexClient("PUBLIC_KEY", "SECRET_KEY", True)

    # print(bitmex.contracts['XBTUSD'].base_asset, bitmex.contracts['XBTUSD'].price_decimals)
    # print(bitmex.balances['XBt'].wallet_balance)
    # print(bitmex.place_order(bitmex.contracts['XBTUSD'], "Limit", 50, "Buy",
                             # price=20000, tif="GoodTillCancel"))


    root = tk.Tk()
    root.mainloop()
