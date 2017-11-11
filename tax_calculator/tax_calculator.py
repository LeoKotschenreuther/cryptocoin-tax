from datetime import timedelta

from .utils import AssetSale

WASH_SALE_DAYS = 30


def _extract_transactions(exchanges):
    transactions = {}
    for exchange in exchanges:
        for key, values in exchange.getTransactions().items():
            if key not in transactions:
                transactions[key] = []
            transactions[key] += values
    return transactions


def _is_wash_sale_lot(sale, buy):
    days_difference = abs((sale.created_at_date - buy.created_at_date).days)
    return days_difference <= WASH_SALE_DAYS


def _wash_sale_lots(sale, lots):
    return [lot for lot in lots if _is_wash_sale_lot(sale, lot)]


def _process_sale(transaction, lots):
    asset_sales = []
    while transaction.amount > 0:
        lot = max(lots, key=lambda lot: lot.price)
        asset_sale = None
        if transaction.amount >= lot.amount:
            proceeds = lot.amount / transaction.amount * transaction.total
            asset_sale = AssetSale(
                property=transaction.currency,
                aquired_at=lot.created_at,
                sold_at=transaction.created_at,
                proceeds=proceeds,
                basis=lot.total
            )
            lots.remove(lot)
            transaction.amount -= lot.amount
            transaction.total -= proceeds
        elif lot.amount > transaction.amount:
            basis = transaction.amount / lot.amount * lot.total
            asset_sale = AssetSale(
                property=transaction.currency,
                aquired_at=lot.created_at,
                sold_at=transaction.created_at,
                proceeds=transaction.total,
                basis=basis
            )
            lot.amount -= transaction.amount
            lot.total -= basis
            transaction.amount = 0
        if asset_sale.is_loss():
            wash_sale_lots = _wash_sale_lots(transaction, lots)
            if wash_sale_lots:
                chosen_lot = min(wash_sale_lots, key=lambda lot: lot.price)
                # todo:
                # increase holding period of chosen_lot by holding_period of
                # asset_sale
                # this is important to differ between long term and short term
                # holdings

                # asset_sale.gain_loss is a negative number, hence we add the
                # loss as a cost to the chosen_lot by subtracting
                chosen_lot.total -= asset_sale.gain_loss
                asset_sale.gain_loss = 0
                # todo:
                # add info about wash sale to asset_sale
        asset_sales.append(asset_sale)
    return asset_sales


def calculate_taxes(exchanges):
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
