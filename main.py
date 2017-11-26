import profig

from exchanges import *
from tax_calculator import *

CONFIG_FILE = 'config.cfg'


def init_exchanges(config):
    config_keys = config.as_dict(dict_type=dict).keys()
    exchanges = []

    if 'bittrex' in config_keys:
        bittrex = Bittrex(config['bittrex.csv_file'], GDAXPublic())
        exchanges.append(bittrex)
    if 'coinbase' in config_keys:
        coinbase = Coinbase(config['coinbase.key'], config['coinbase.secret'])
        exchanges.append(coinbase)
    if 'gdax' in config_keys:
        gdaxPrivate = GDAXPrivate(config['gdax.key'], config['gdax.secret'],
                                  config['gdax.passphrase'])
        exchanges.append(gdaxPrivate)
    if 'kraken' in config_keys:
        kraken = Kraken(config['kraken.key'], config['kraken.secret'],
                        GDAXPublic())
        exchanges.append(kraken)
    if 'poloniex' in config_keys:
        poloniex = Poloniex(config['poloniex.key'], config['poloniex.secret'],
                            GDAXPublic())
        exchanges.append(poloniex)

    return exchanges

if __name__ == '__main__':
    config = profig.Config(CONFIG_FILE)
    config.sync()

    exchanges = init_exchanges(config)

    asset_sales, leftover_lots = calculate_gains_losses(exchanges)

    total_gain_loss = sum(sale.gain_loss for sale in asset_sales)
    print("total gains/loss:")
    print("{} USD".format(total_gain_loss))

    for lot in leftover_lots:
        print(lot.currency, lot.created_at, lot.amount, lot.price)
