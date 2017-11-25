import datetime
import poloniex

from .utils import Transaction


PRECISION = 8


class Poloniex(object):
    def __init__(self, key, secret, gdaxAPI):
        self._key = key
        self._secret = secret
        self._gdax = gdaxAPI

    # _client creates and returns a Poloniex client
    def _client(self):
        return poloniex.Poloniex(self._key, self._secret)

    # _opposite_side returns the opposite of the given side
    def _opposite_side(self, side):
        if side == 'sell':
            return 'buy'
        return 'sell'

    # _to_timestamp converts the given string to a python timestamp object
    def _to_timestamp(self, ts_string):
        return datetime.datetime.strptime(ts_string, "%Y-%m-%d %H:%M:%S")

    # getTransactions pulls all transactions from the GDAX API
    def getTransactions(self):
        client = self._client()
        transactions = {}
        start_date = datetime.datetime(datetime.datetime.now().year, 1, 1)
        fills = client.returnTradeHistory(start=start_date.timestamp())
        for key, history in fills.items():
            underscore_position = key.index("_")
            currency = key[underscore_position + 1:].upper()
            base_currency = key[:underscore_position].upper()
            if currency not in transactions:
                transactions[currency] = []
            if base_currency not in transactions:
                transactions[base_currency] = []
            for transaction in history:
                # first the currency that was traded
                transaction_ts = self._to_timestamp(transaction['date'])
                base_amount = transaction['total']
                base_price = self._gdax.getHistoryPrice(base_currency,
                                                        transaction_ts)
                c_t = Transaction(
                    side=transaction['type'],
                    currency=currency,
                    created_at=transaction_ts,
                    amount=transaction['amount'],
                    base_amount=base_amount,
                    base_price=base_price
                )
                if transaction['type'] == 'buy':
                    c_t.fee_paid_in_currency(transaction['fee'], PRECISION)
                transactions[currency].append(c_t)
                # now the base currency, something like btc or eth
                transactions[base_currency].append(Transaction(
                    side=self._opposite_side(transaction['type']),
                    currency=base_currency,
                    created_at=transaction_ts,
                    amount=base_amount,
                    base_amount=base_amount,
                    base_price=base_price
                ))
        return transactions
