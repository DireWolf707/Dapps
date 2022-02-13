from scripts.utils import get_account,export_contract,get_contract,fund_with_link
from brownie import Lottery,config,network
import time

def deploy(export=False):
    account = get_account()
    print("deploying lottery contract!")
    contract = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf").address,
        get_contract("link").address,
        config["networks"][network.show_active()]["key_hash"],
        config["networks"][network.show_active()]["fee"]*10**18,
        {
            "from":account
        }
    )
    print("Lottery contract deployed!")
    # remember to fund with LINK
    fund_with_link(contract.address,amount=0.5*10**18)
    if export:
        export_contract(contract)

def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx = lottery.startLottery({"from":account})
    tx.wait(1)
    print("Lottery started")

def entry_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee()
    tx = lottery.enter({"from":account,"value":value})
    tx.wait(1)
    print("You entered the lottery")

def end_lottery():
    account = get_account()
    lottery = Lottery[-1] 
    #funding link
    fund_with_link(lottery.address)
    tx = lottery.endLottery({"from":account})
    tx.wait(1)
    time.sleep(15)
    print("Last winner:",lottery.lastWinner())

def main():
    deploy(export=True)
