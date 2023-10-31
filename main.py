import tkinter as tk
import logging

from connectors.binance_futures import BinanceFuturesClient

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

    binance = BinanceFuturesClient("335b56bcfa680f9e05da471dd9e9bc4405d7314b98c763ad4c5bbb0d88d0a268","489245401743d4fa727b55e1b104d928c44880a1466758db5e34e0ac89343c40", True)
    # print(binance.get_contracts())
    # print(binance.get_bid_ask("BTCUSDT"))
    print(binance.get_historical_candles("BTCUSDT", "1h"))

    root = tk.Tk()
    root.mainloop()

