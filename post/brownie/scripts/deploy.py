from brownie import Posts,config,network
from scripts.utils import get_account,export_contract

def deploy(export=False):
    account = get_account()
    price_feed_address = config["networks"][network.show_active()]["pricefeed"]
    contract = Posts.deploy(price_feed_address,{
        "from":account
    })
    if export:
        export_contract(contract)

def main():
    deploy(export=True)