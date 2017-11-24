import profig

from exchanges import *
from tax_calculator import *

CONFIG_FILE = 'config.cfg'

if __name__ == '__main__':
    config = profig.Config(CONFIG_FILE)
    config.sync()

    config_keys = config.as_dict(dict_type=dict).keys()
    exchanges = []

    if 'coinbase' in config_keys:
        coinbase = Coinbase(config['coinbase.key'], config['coinbase.secret'])
        exchanges.append(coinbase)
    if 'gdax' in config_keys:
        gdax = GDAX(config['gdax.key'], config['gdax.secret'],
                    config['gdax.passphrase'])
        exchanges.append(gdax)
    if 'poloniex' in config_keys:
        poloniex = Poloniex(config['poloniex.key'], config['poloniex.secret'],
                            gdax)
        exchanges.append(poloniex)

    asset_sales, _ = calculate_gains_losses(exchanges)

    total_gain_loss = sum(sale.gain_loss for sale in asset_sales)
    print("total gains/loss:")
    print("{} USD".format(total_gain_loss))

    # for lot in leftover_lots:
    #     print(lot.currency, lot.amount, lot.price)
