from scripts.utils import get_account,export_contract
from brownie import Voting

def deploy(export=False):
    account = get_account()
    contract = Voting.deploy({
        "from":account
    })
    if export:
        export_contract(contract)

def main():
    deploy(export=True)