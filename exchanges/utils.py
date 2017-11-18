from datetime import datetime
from decimal import Decimal


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

    # created_at_date returns the create_at value as a date
    @property
    def created_at_date(self):
        return datetime.strptime(self.created_at[:10], "%Y-%m-%d").date()

    # price returns the price per share of the Transaction
    @property
    def price(self):
        return self.total / self.amount
