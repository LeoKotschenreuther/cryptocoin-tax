import profig

from exchanges import *

CONFIG_FILE = 'config.cfg'

if __name__ == '__main__':
    config = profig.Config(CONFIG_FILE)
    config.sync()

    coinbase = Coinbase(config['coinbase.key'], config['coinbase.secret'])
    transactions = coinbase.getTransactions()
    print(transactions)
