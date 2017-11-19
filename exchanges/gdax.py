import datetime
import gdax

from .utils import Transaction


class GDAX(object):
    def __init__(self, key, secret, passphrase):
        self._passphrase = passphrase
        self._key = key
        self._secret = secret
        self._client = None

    # _client creates and returns a GDAX client
    def _get_client(self):
        if not self._client:
            self._client = gdax.AuthenticatedClient(self._key, self._secret,
                                                    self._passphrase)
        return self._client

    # _to_timestamp converts the given string to a python timestamp object
    def _to_timestamp(self, ts_string):
        return datetime.datetime.strptime(ts_string[:19], "%Y-%m-%dT%H:%M:%S")

    # getHistoryPrice the price for the specified currency for a given
    # timestamp from GDAX
    def getHistoryPrice(self, currency, ts):
        client = self._get_client()
        start = ts - datetime.timedelta(seconds=ts.second)
        end = ts.replace(second=59)
        data = None
        for _ in range(3):
            data = client.get_product_historic_rates(currency + '-USD',
                                                     start=start.isoformat(),
                                                     end=end.isoformat(),
                                                     granularity=60)
            if data:
                break
        return data[0][4]

    # getTransactions pulls all transactions from the GDAX API
    def getTransactions(self):
        client = self._get_client()
        transactions = {}
        fills = client.get_fills()
        for page in fills:
            valid_fills = (fill for fill in page if fill['settled'])
            for fill in valid_fills:
                minus_position = fill['product_id'].index("-")
                currency = fill['product_id'][:minus_position].upper()
                if currency not in transactions:
                    transactions[currency] = []
                transactions[currency].append(Transaction(
                    side=fill['side'],
                    currency=currency,
                    created_at=self._to_timestamp(fill['created_at']),
                    amount=fill['size'],
                    price=fill['price'],
                    fee=fill['fee']
                ))
        return transactions
