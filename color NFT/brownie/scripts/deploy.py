from scripts.utils import get_account,export_contract
from brownie import ColorNFT

def deploy(export=False):
    account = get_account()
    contract = ColorNFT.deploy({
        "from":account
    })
    if export:
        export_contract(contract)

def main():
    deploy(export=True)