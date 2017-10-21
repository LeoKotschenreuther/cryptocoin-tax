from coinbase.wallet.client import Client
from .utils import Transaction


class Coinbase(object):
    def __init__(self, key, secret):
        self._key = key
        self._secret = secret

    def _client(self):
        return Client(self._key, self._secret)

    def getTransactions(self):
        client = self._client()
        accounts = client.get_accounts()
        transaction_accounts = (account for account in accounts['data']
                                if account['type'] == 'wallet')
        transactions = {}
        for account in transaction_accounts:
            currency = account['currency']
            transactions[currency] = []
            valid_buys = (buy for buy in client.get_buys(account['id'])['data']
                          if buy['committed'])
            for buy in valid_buys:
                transactions[currency].append(Transaction(
                    side='buy',
                    currency=currency,
                    created_at=buy['created_at'],
                    amount=buy['amount']['amount'],
                    total=buy['total']['amount'])
                )
            valid_sells = (sell for sell
                           in client.get_sells(account['id'])['data']
                           if sell['committed'])
            for sell in valid_sells:
                transactions[currency].append(Transaction(
                    side='sell',
                    currency=currency,
                    created_at=sell['created_at'],
                    amount=sell['amount']['amount'],
                    total=sell['total']['amount'])
                )
        return transactions
