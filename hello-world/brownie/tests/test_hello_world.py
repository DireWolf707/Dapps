from scripts.deploy import deploy
from scripts.utils import get_account
from brownie import HelloWorld

def test_changeData():
    account = get_account()
    deploy()
    contract = HelloWorld[-1]
    
    data = contract.data()
    assert data == "world"

    new_data = "everyone"
    tx = contract.changeData(new_data,{
        "from":account
    })
    tx.wait(1)
    data = contract.data()
    assert data == new_data