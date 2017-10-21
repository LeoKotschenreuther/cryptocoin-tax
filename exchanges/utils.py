from decimal import *


class Transaction(object):
    def __init__(self, side, currency, created_at, amount, total=None,
                 price=None, fee=None):
        self.side = side
        self.currency = currency
        self.created_at = created_at
        self.amount = Decimal(amount)
        if total:
            self.total = Decimal(total)
        elif price and fee:
            self.total = Decimal(amount) * Decimal(price) + Decimal(fee)

    @property
    def price(self):
        return self.total / self.amount
