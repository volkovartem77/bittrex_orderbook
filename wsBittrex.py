import json
import threading
import time
import traceback
from base64 import b64decode
from urllib.parse import quote_plus
from zlib import decompress, MAX_WBITS

import requests
import websocket


NAME = 'Bittrex'


class BittrexWebsocket:

    def __init__(self, symbol):
        """Constructor"""
        self.__symbol = symbol
        self.__token = ""
        self.__orderbook_bid = {}
        self.__orderbook_ask = {}
        self.__ws = None

        # Constants
        self.__NAME = 'Bittrex'
        self.__REST_ENDPOINT = "https://socket.bittrex.com/signalr/"
        self.__WS_ENDPOINT = "wss://socket.bittrex.com/signalr/"
        self.__TRANSPORT = "webSockets"
        self.__CLIENT_PROTOCOL = "1.5"
        self.__CONNECTION_DATA = "%5B%7B%22name%22%3A%22c2%22%7D%5D"

    def __get_conn_token(self):
        r = requests.get(f'{self.__REST_ENDPOINT}negotiate?'
                         f'clientProtocol={self.__CLIENT_PROTOCOL}&'
                         f'connectionData={self.__CONNECTION_DATA}'
                         f'&_={time.time()}')
        if r is not None:
            self.__token = quote_plus(json.loads(r.text)['ConnectionToken'])
        self.__TID = "3"

    def __start_ws(self):
        self.__get_conn_token()
        r = requests.get(
            f'{self.__REST_ENDPOINT}start?'
            f'transport={self.__TRANSPORT}&'
            f'clientProtocol={self.__CLIENT_PROTOCOL}&'
            f'connectionToken={self.__token}&'
            f'connectionData={self.__CONNECTION_DATA}&'
            f'_={time.time()}'
        )
        if r is not None:
            if json.loads(r.text)['Response'] == 'started':
                return True
        return False

    @staticmethod
    def __process_message(message):
        try:
            deflated_msg = decompress(b64decode(message, validate=True), -MAX_WBITS)
        except SyntaxError:
            deflated_msg = decompress(b64decode(message, validate=True))
        return json.loads(deflated_msg.decode())

    def __on_message(self, message):
        message = json.loads(message)
        # print(message)

        if "R" in message:
            message = self.__process_message(message['R'])
            # print(message)
            self.__orderbook_bid = dict((x['R'], x['Q']) for x in message['Z'])
            self.__orderbook_ask = dict((x['R'], x['Q']) for x in message['S'])

        if "M" in message and len(message['M']) > 0:
            message = message["M"][0]
            if 'A' in message and len(message['A']) > 0:
                message = self.__process_message(message['A'][0])
                # print(message)

                for x in message['Z']:
                    if x['TY'] == 0 or x['TY'] == 2:
                        self.__orderbook_bid.update({x['R']: x['Q']})
                    if x['TY'] == 1:
                        self.__orderbook_bid.pop(x['R'])
                for x in message['S']:
                    if x['TY'] == 0 or x['TY'] == 2:
                        self.__orderbook_ask.update({x['R']: x['Q']})
                    if x['TY'] == 1:
                        self.__orderbook_ask.pop(x['R'], None)

                ask = list(sorted(self.__orderbook_ask.keys()))[0]
                bid = list(sorted(self.__orderbook_bid.keys(), reverse=True))[0]
                bid_amount = self.__orderbook_bid[bid]
                ask_amount = self.__orderbook_ask[ask]

                print(self.__symbol, json.dumps({
                    'bid': bid,
                    'ask': ask,
                    'bid_amount': bid_amount,
                    'ask_amount': ask_amount,
                    'timestamp': int(time.time() * 1000)
                }))

                # print(self.__orderbook_bid)
                # print(self.__orderbook_ask)

    def __on_error(self, error):
        print(f'ws{self.__NAME}: {error}')

    def __on_close(self):
        print(f'ws{self.__NAME}: {"closed"}')

    def __on_open(self):
        print(f'ws{self.__NAME} subscribe {self.__symbol}')

        symbol = self.__symbol.split('_')[1] + '-' + self.__symbol.split('_')[0]
        self.__ws.send(json.dumps({"H": "c2", "M": "SubscribeToExchangeDeltas", "A": [symbol], "I": 3}))
        self.__ws.send(json.dumps({"H": "c2", "M": "QueryExchangeState", "A": [symbol], "I": 7}))

    def run(self):
        if self.__start_ws():
            self.__ws = websocket.WebSocketApp(
                f"{self.__WS_ENDPOINT}connect?"
                f"transport={self.__TRANSPORT}&"
                f"clientProtocol={self.__CLIENT_PROTOCOL}&"
                f"connectionToken={self.__token}&"
                f"connectionData={self.__CONNECTION_DATA}",
                on_open=self.__on_open,
                on_message=self.__on_message,
                on_error=self.__on_error,
                on_close=self.__on_close)

            self.__ws.run_forever()


def run_ws(symbol):
    bittrex = BittrexWebsocket(symbol)
    bittrex.run()


if __name__ == "__main__":
    try:
        SYMBOLS = ['ETH_BTC',
                   'ETH_USDT',
                   'BTC_USDT',
                   'LTC_BTC',
                   'LTC_ETH',
                   'LTC_USDT'
                   ]

        print(f'ws{NAME}: start')

        for s in SYMBOLS:
            th = threading.Thread(target=run_ws, kwargs={'symbol': s})
            th.start()
    except KeyboardInterrupt:
        exit()
    except:
        print(traceback.format_exc())
