import krakenex
import datetime

from .utils import Transaction


class Kraken(object):
    def __init__(self, key, secret, gdaxAPI):
        self._key = key
        self._secret = secret
        self._gdax = gdaxAPI

    # _client creates and returns a Kraken client
    def _client(self):
        return krakenex.API(key=self._key, secret=self._secret)

    # _opposite_side returns the opposite of the given side
    def _opposite_side(self, side):
        if side == 'sell':
            return 'buy'
        return 'sell'

    # _to_timestamp converts the given string to a python timestamp object
    def _to_timestamp(self, ts):
        return datetime.datetime.utcfromtimestamp(ts)

    # getTransactions pulls all transactions from the Kraken API
    def getTransactions(self):
        client = self._client()
        trades = client.query_private('TradesHistory')

        transactions = {}
        for trade in trades['result']['trades'].values():
            pair = trade['pair'][1:]
            x_position = pair.index("X")
            currency = pair[:x_position].upper()
            base_currency = pair[x_position + 1:].upper()
            if currency not in transactions:
                transactions[currency] = []
            if base_currency not in transactions:
                transactions[base_currency] = []
            # first the currency that was traded
            trade_ts = self._to_timestamp(trade['time'])
            base_amount = trade['cost']
            base_price = self._gdax.getHistoryPrice(base_currency,
                                                    trade_ts)
            c_t = Transaction(
                side=trade['type'],
                currency=currency,
                created_at=trade_ts,
                amount=trade['vol'],
                base_amount=base_amount,
                base_price=base_price
            )
            transactions[currency].append(c_t)
            # now the base currency, something like btc or eth
            transactions[base_currency].append(Transaction(
                side=self._opposite_side(trade['type']),
                currency=base_currency,
                created_at=trade_ts,
                amount=base_amount,
                base_amount=base_amount,
                base_price=base_price
            ))
        return transactions
