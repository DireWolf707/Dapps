from brownie import HelloWorld
from scripts.utils import get_account

def main():
    account = get_account()
    contract = HelloWorld[-1]
    new_data = input("Enter new data:")
    tx = contract.changeData(new_data,{
        "from":account
    })
    tx.wait(1)
