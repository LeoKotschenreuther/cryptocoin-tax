# Cryptocoin Tax

A tool to calculate the gains and losses of your blockchain investments to help figure out how much tax you owe.

## Idea

This tool will help you figure out the gains and losses of your blockchain investments. The most convenient way to get all the needed data is to create API keys for all the exchanges you used during the year you would like to calculate your gains and losses for. Additionally, this tool will distinguish between short and long term investments, depending on whether you held your investment for less or more than a year.

## Dependencies

The few dependencies are [Python3](https://www.python.org/download/releases/3.0/) and a couple of python packages. It helps to set up a [virtualenv](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/) first. The following instructions assume that you have already installed Python and pip. Start with installing virtualenv and then create a virtual environment in this folder:

```sh
pip install virtualenv
virtualenv -p python3 .venv
```

Now activate the virtual environment with:

```sh
source .venv/bin/activate
```

Finally it's time to install all the required pip packages. Pip doesn't find the poloniex package so we have to provide the link manually:

```sh
pip install https://github.com/s4w3d0ff/python-poloniex/archive/v0.4.6.zip
pip install -r requirements.txt
```

## Config

Copy the file `sample_config.cfg` and name the new version `config.cfg`. This is used to handle all the API keys. Open the newly created file and put in your actual API keys.

## Collecting data from all the exchanges

As of now, the following exchanges are supported:

* Bittrex
* Coinbase
* GDAX
* Kraken
* Poloniex

For most of the exchanges, you just have to create an API key with the proper read authorization. However, since Bittrex doesn't support to pull all the transactions, you need to download the transaction history from Bittrex as a csv file. Place that file in the `data` directory and specify the exact location in the config file.

## Running the program

You can execute the program with the following command:

```bash
python main.py
```
