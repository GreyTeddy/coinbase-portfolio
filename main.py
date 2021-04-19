from dotenv import load_dotenv
from os import environ, system, name
from time import sleep, ctime
import crypto
import sys
sys.modules['Crypto'] = crypto
from coinbase.wallet.client import Client

tokens = load_dotenv()

api_key = environ.get("api_key")
api_secret = environ.get("api_secret")

client = Client(api_key,
                api_secret,
                api_version='2020-3-17')

# convert to gbp
def currency_to_gbp(currency,exchange_rates):
    return 1/float(exchange_rates[currency])*float(exchange_rates["GBP"])

def print_portfolio(client):
    # get exchange info
    exchange_rates = client.get_exchange_rates()["rates"]

    # get info for each account that has balance
    accounts = client.get_accounts()["data"]
    accounts.append(client.get_primary_account())

    total = 0
    for i in accounts:
        crypt_amount = float(i["balance"]["amount"])
        if crypt_amount > 0:
            crypto_price = currency_to_gbp(i["balance"]["currency"],exchange_rates)
            crypto_balance = round(crypto_price*crypt_amount,2)
            print("{}: £{}".format(i["balance"]["currency"],crypto_balance),"({})".format(crypt_amount))
            total += crypto_balance
    print("Total: £{}".format(round(total,2)))

def clear_console():
    if name == "nt":
        system("cls")
    else:
        system("clear")

while True:
    print(ctime())
    print_portfolio(client)
    sleep(10)
    clear_console()