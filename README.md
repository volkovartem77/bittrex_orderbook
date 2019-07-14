## Bittrex websocket order book in Python 

**This code aimed to help programmers update Bittrex orderbook
quickly through websocket.\
This class manages increment data\
You can subscribe to multiple pairs at the same time and
get Asks and Bids.**

### Simple usage

Basically it's just a class, so you can just copy BittrexWebsocket class and use it this way:
```python
bittrex = BittrexWebsocket('ETH_BTC')
bittrex.run()
```

Or you can run a cycle if you want to subscribe to multiple pairs:
```python
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

        for s in SYMBOLS:
            th = threading.Thread(target=run_ws, kwargs={'symbol': s})
            th.start()
    except KeyboardInterrupt:
        exit()
    except:
        print(traceback.format_exc())
```

As result:
```text
wsBittrex: start
wsBittrex subscribe LTC_ETH
wsBittrex subscribe BTC_USDT
wsBittrex subscribe LTC_USDT
wsBittrex subscribe ETH_BTC
wsBittrex subscribe LTC_BTC
wsBittrex subscribe ETH_USDT
LTC_ETH {"bid": 0.37483783, "ask": 0.37644154, "bid_amount": 4.53309274, "ask_amount": 3.0642521, "timestamp": 1563066505541}
ETH_BTC {"bid": 0.02366281, "ask": 0.02370031, "bid_amount": 1.28850673, "ask_amount": 8.44467184, "timestamp": 1563066505567}
ETH_USDT {"bid": 267.33195115, "ask": 267.78325446, "bid_amount": 13.35993796, "ask_amount": 0.1877301, "timestamp": 1563066505573}
LTC_BTC {"bid": 0.00889971, "ask": 0.0089047, "bid_amount": 40.08862236, "ask_amount": 0.59163262, "timestamp": 1563066505574}
LTC_BTC {"bid": 0.00889971, "ask": 0.0089047, "bid_amount": 40.08862236, "ask_amount": 0.59163262, "timestamp": 1563066505611}
ETH_BTC {"bid": 0.02366281, "ask": 0.02370031, "bid_amount": 1.28850673, "ask_amount": 8.44467184, "timestamp": 1563066505613}
LTC_ETH {"bid": 0.37483783, "ask": 0.37644153, "bid_amount": 4.53309274, "ask_amount": 0.59163262, "timestamp": 1563066505614}
BTC_USDT {"bid": 11279.39800001, "ask": 11293.092, "bid_amount": 0.5, "ask_amount": 0.00079229, "timestamp": 1563066505619}
LTC_USDT {"bid": 100.44325938, "ask": 100.77199999, "bid_amount": 292.95408407, "ask_amount": 76.62555449, "timestamp": 1563066505627}
ETH_USDT {"bid": 267.33195115, "ask": 267.78325446, "bid_amount": 13.35993796, "ask_amount": 0.1877301, "timestamp": 1563066505635}
BTC_USDT {"bid": 11279.39800001, "ask": 11293.092, "bid_amount": 0.5, "ask_amount": 0.00079229, "timestamp": 1563066505638}
LTC_ETH {"bid": 0.37483783, "ask": 0.37644153, "bid_amount": 4.53309274, "ask_amount": 0.59163262, "timestamp": 1563066505853}
LTC_BTC {"bid": 0.00889971, "ask": 0.0089047, "bid_amount": 40.08862236, "ask_amount": 0.59163262, "timestamp": 1563066505862}
ETH_BTC {"bid": 0.02366281, "ask": 0.02370031, "bid_amount": 1.28850673, "ask_amount": 8.44467184, "timestamp": 1563066505863}
```

It is latest bid and ask, and their amounts, but you can get full orderbook if you pay 
attention to this code:
```python
print(self.__orderbook_bid)
print(self.__orderbook_ask)
```
There are 2 objects where orderbook for Ask and Bid stored. Enjoy.