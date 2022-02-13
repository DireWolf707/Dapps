import pytest,time
from brownie import Posts,accounts
from brownie.exceptions import VirtualMachineError
from scripts.deploy import deploy
from web3 import Web3

def test_deploy():
    assert len(Posts) == 0
    deploy()
    assert len(Posts) == 1

def test_post():
    contract = Posts[-1]
    acc1 = accounts[0]
    acc2 = accounts[1]

    assert len(contract.getPosts()) == 0

    with pytest.raises(VirtualMachineError):
        contract.createPost("title","",{"from":acc1})

    with pytest.raises(VirtualMachineError):
        contract.createPost("","content",{"from":acc1})

    assert len(contract.getPosts()) == 0
    contract.createPost("title","content",{"from":acc1})
    assert len(contract.getPosts()) == 1

    with pytest.raises(VirtualMachineError):
        contract.updatePost("","content",0,{"from":acc1})

    with pytest.raises(VirtualMachineError):
        contract.updatePost("title","",0,{"from":acc1})
    
    with pytest.raises(VirtualMachineError):
        contract.updatePost("title","content",1,{"from":acc1})

    with pytest.raises(VirtualMachineError):
        contract.updatePost("title","content",0,{"from":acc2})

    contract.updatePost("title#","content#",0,{"from":acc1})
    assert len(contract.getPosts()) == 1

    post = contract.posts(0)
    assert post[0] == "title#"
    assert post[1] == "content#"

    with pytest.raises(VirtualMachineError):
        contract.tipPost(0,{"from":acc1})
    
    with pytest.raises(VirtualMachineError):
        contract.tipPost(1,{"from":acc2})

    beforeTipBalance = acc1.balance()
    tipAmount = Web3.toWei(2,"ether")
    contract.tipPost(0,{"from":acc2,"amount":tipAmount})
    afterTipBalance = acc1.balance()

    assert beforeTipBalance + tipAmount == afterTipBalance

    post = contract.posts(0)
    assert post[2] == tipAmount

    time.sleep(1)