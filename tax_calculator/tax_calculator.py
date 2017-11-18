from datetime import timedelta

from .utils import AssetSale

WASH_SALE_DAYS_LIMIT = 30


# _extract_transactions pulls all transactions from the specified exchanges and
# groups them by currencies
def _extract_transactions(exchanges):
    transactions = {}
    for exchange in exchanges:
        for key, values in exchange.getTransactions().items():
            if key not in transactions:
                transactions[key] = []
            transactions[key] += values
    return transactions


# _is_wash_sale_time_period returns whether the two given dates are within the
# wash sale time period
def _is_wash_sale_time_period(sale_date, buy_date):
    days_difference = abs((sale_date - buy_date).days)
    return days_difference <= WASH_SALE_DAYS_LIMIT


# _wash_sale_lots selects all lots that were bought within the wash sale time
# period of the sale_date
def _wash_sale_lots(sale_date, lots):
    return [lot for lot in lots
            if _is_wash_sale_time_period(sale_date, lot.created_at_date)]


# _process_sale calculates the gain or loss of the specified sale considering
# the given lots. It also applies a wash sale if necessary.
def _process_sale(sale, lots):
    asset_sales = []
    while sale.amount > 0:
        lot = max(lots, key=lambda lot: lot.price)
        asset_sale = AssetSale(
            property=sale.currency,
            aquired_at=lot.created_at,
            sold_at=sale.created_at
        )
        # the chosen lot is being used up completley for this sale
        if sale.amount >= lot.amount:
            proceeds = lot.amount / sale.amount * sale.total
            asset_sale.proceeds = proceeds
            asset_sale.basis = lot.total
            lots.remove(lot)
            sale.amount -= lot.amount
            sale.total -= proceeds
        # only part of the chosen lot is used for this sale
        else:
            basis = sale.amount / lot.amount * lot.total
            asset_sale.proceeds = sale.total
            asset_sale.basis = basis
            lot.amount -= sale.amount
            lot.total -= basis
            sale.amount = 0
        # if asset_sale.is_loss():
        #     wash_sale_lots = _wash_sale_lots(sale.created_at_date, lots)
        #     if wash_sale_lots:
        #         # todo:
        #         # calculate wash sale by number of shares
        #         chosen_lot = min(wash_sale_lots, key=lambda lot: lot.price)
        #         # todo:
        #         # increase holding period of chosen_lot by holding_period of
        #         # asset_sale
        #         # this is important to differ between long term and short term
        #         # holdings

        #         # asset_sale.gain_loss is a negative number, hence we add the
        #         # loss as a cost to the chosen_lot by subtracting
        #         chosen_lot.total -= asset_sale.gain_loss
        #         asset_sale.gain_loss = 0
        #         # todo:
        #         # add info about wash sale to asset_sale
        asset_sales.append(asset_sale)
    return asset_sales


# calculate_gains_losses calculates the gains and losses for all the
# transactions from the given exchanges
def calculate_gains_losses(exchanges):
    transactions = _extract_transactions(exchanges)

    asset_sales = []
    for currency, c_transactions in transactions.items():
        lots = []
        c_transactions.sort(key=lambda transaction: transaction.created_at)
        for transaction in c_transactions:
            if transaction.side == 'buy':
                lots.append(transaction)
            elif transaction.side == 'sell':
                asset_sales += _process_sale(transaction, lots)
    return asset_sales
