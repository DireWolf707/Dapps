import pytest
from brownie import Fund,accounts, web3
from brownie.exceptions import VirtualMachineError
from scripts.deploy import deploy
from web3 import Web3
def test_deploy():
    assert len(Fund) == 0
    deploy()
    assert len(Fund) == 1

def test_fund():
    contract = Fund[-1]
    acc1 = accounts[0]
    acc2 = accounts[1]
    acc3 = accounts[2]

    assert contract.count() == 0

    assert contract.isOwner({"from":acc1}) == True
    assert contract.isOwner({"from":acc2}) == False

    with pytest.raises(VirtualMachineError):
        contract.currentFunds({"from":acc2})

    assert contract.currentFunds({"from":acc1}) == 0

    fund_amount = Web3.toWei(1,"ether")
    contract.fund({"from":acc2,"value":fund_amount})

    assert contract.currentFunds({"from":acc1}) == fund_amount
    assert contract.count() == 1
    assert contract.topFunder() == acc2.address

    contract.fund({"from":acc3,"value":fund_amount/10})

    assert contract.currentFunds({"from":acc1}) == fund_amount + fund_amount/10
    assert contract.count() == 2
    assert contract.topFunder() == acc2.address

    contract.fund({"from":acc3,"value":fund_amount})

    assert contract.currentFunds({"from":acc1}) == fund_amount*2 + fund_amount/10
    assert contract.count() == 3
    assert contract.topFunder() == acc3.address

    with pytest.raises(VirtualMachineError):
        contract.withdraw({"from":acc2})

    prev_balance = acc1.balance()
    contract.withdraw({"from":acc1})
    after_balance = acc1.balance()

    assert after_balance > prev_balance + fund_amount
    assert contract.currentFunds({"from":acc1}) == 0
