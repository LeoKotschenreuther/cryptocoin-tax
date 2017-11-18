import gdax

from .utils import Transaction


class GDAX(object):
    def __init__(self, key, secret, passphrase):
        self._passphrase = passphrase
        self._key = key
        self._secret = secret

    # _client creates and returns a GDAX client
    def _client(self):
        return gdax.AuthenticatedClient(self._key, self._secret,
                                        self._passphrase)

    # getTransactions pulls all transactions from the GDAX API
    def getTransactions(self):
        client = self._client()
        transactions = {}
        fills = client.get_fills()
        for page in fills:
            valid_fills = (fill for fill in page if fill['settled'])
            for fill in valid_fills:
                currency = fill['product_id'][:3].lower()
                if currency not in transactions:
                    transactions[currency] = []
                transactions[currency].append(Transaction(
                    side=fill['side'],
                    currency=currency,
                    created_at=fill['created_at'],
                    amount=fill['size'],
                    price=fill['price'],
                    fee=fill['fee']
                ))
        return transactions
