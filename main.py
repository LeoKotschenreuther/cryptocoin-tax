import profig

from exchanges import *
from tax_calculator import *

CONFIG_FILE = 'config.cfg'

if __name__ == '__main__':
    config = profig.Config(CONFIG_FILE)
    config.sync()

    coinbase = Coinbase(config['coinbase.key'], config['coinbase.secret'])
    gdax = GDAX(config['gdax.key'], config['gdax.secret'],
                config['gdax.passphrase'])
    poloniex = Poloniex(config['poloniex.key'], config['poloniex.secret'],
                        gdax)
    # poloniex.getTransactions()

    asset_sales, _ = calculate_gains_losses([coinbase, gdax, poloniex])

    total_gain_loss = sum(sale.gain_loss for sale in asset_sales)
    print("total gains/loss:")
    print("{} USD".format(total_gain_loss))

    # for lot in leftover_lots:
    #     print(lot.currency, lot.amount, lot.price)
