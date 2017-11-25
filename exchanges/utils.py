from datetime import datetime
from decimal import Decimal


class Transaction(object):
    def __init__(self, side, currency, created_at, amount, total=None,
                 price=None, fee=None, base_amount=None, base_price=None):
        self.side = side
        self.currency = currency
        self.created_at = created_at
        self.amount = Decimal(amount)
        if total:
            self.total = Decimal(total)
        elif price and fee:
            self.total = Decimal(amount) * Decimal(price) + Decimal(fee)
        # when a non fiat currency like btc or eth was used to buy/ sell the
        # given currency into
        elif base_amount and base_price:
            self.total = Decimal(base_amount) * Decimal(base_price)

    # when the fee was paid in the same currency as the transaction currency
    # and the fee is just specified as a percentage of the amount
    def fee_paid_in_currency(self, fee_percent, precision=None):
        fee = self.amount * Decimal(fee_percent)
        if precision:
            fee = round(fee, precision)
        self.amount -= fee

    # price returns the price per share of the Transaction
    @property
    def price(self):
        return self.total / self.amount
