import profig

from exchanges import *

CONFIG_FILE = 'config.cfg'


class AssetSale(object):
    def __init__(self, property, aquired_at, sold_at, proceeds, basis):
        self.property = property
        self.aquired_at = aquired_at
        self.sold_at = sold_at
        self.proceeds = proceeds
        self.basis = basis
        self.gain_loss = proceeds - basis

if __name__ == '__main__':
    config = profig.Config(CONFIG_FILE)
    config.sync()

    coinbase = Coinbase(config['coinbase.key'], config['coinbase.secret'])
    transactions = coinbase.getTransactions()

    gdax = GDAX(config['gdax.key'], config['gdax.secret'],
                config['gdax.passphrase'])
    for key, gdax_transactions in gdax.getTransactions().items():
        if key not in transactions:
            transactions[key] = []
        transactions[key] += gdax_transactions

    asset_sales = []
    for currency, c_transactions in transactions.items():
        lots = []
        c_transactions.sort(key=lambda transaction: transaction.created_at)
        for transaction in c_transactions:
            if transaction.side == 'buy':
                lots.append(transaction)
            elif transaction.side == 'sell':
                while transaction.amount > 0:
                    lot = max(lots, key=lambda lot: lot.price)
                    if transaction.amount >= lot.amount:
                        proceeds = lot.amount / transaction.amount * transaction.total
                        asset_sales.append(AssetSale(
                            property=currency,
                            aquired_at=lot.created_at,
                            sold_at=transaction.created_at,
                            proceeds=proceeds,
                            basis=lot.total
                        ))
                        lots.remove(lot)
                        transaction.amount -= lot.amount
                        transaction.total -= proceeds
                    elif lot.amount > transaction.amount:
                        basis = transaction.amount / lot.amount * lot.total
                        asset_sales.append(AssetSale(
                            property=currency,
                            aquired_at=lot.created_at,
                            sold_at=transaction.created_at,
                            proceeds=transaction.total,
                            basis=basis
                        ))
                        lot.amount -= transaction.amount
                        lot.total -= basis
                        transaction.amount = 0
    total_gain_loss = sum(sale.gain_loss for sale in asset_sales)
    print("total gains/loss:")
    print("{} USD".format(total_gain_loss))
