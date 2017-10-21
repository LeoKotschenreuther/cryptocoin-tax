from decimal import *


class Transaction(object):
    def __init__(self, side, currency, created_at, amount, total):
        self.side = side
        self.currency = currency
        self.created_at = created_at
        self.amount = Decimal(amount)
        self.total = Decimal(total)

    @property
    def price(self):
        return self.total / self.amount