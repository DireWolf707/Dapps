from brownie import ColorNFT,accounts
import pytest
from scripts.deploy import deploy
from brownie.exceptions import VirtualMachineError

def test_deploy():
    assert len(ColorNFT)==0
    deploy()
    assert len(ColorNFT)==1

def test_colorNFT():
    contract = ColorNFT[-1]
    acc1 = accounts[0]
    acc2 = accounts[1]

    color_code_1 = "#C22828"
    color_code_2 = "#B9E6D3"
    color_code_3 = "#F66095"

    assert contract.colorExists(color_code_1) == False
    assert contract.colorExists(color_code_2) == False
    assert contract.colorExists(color_code_3) == False
    assert len(contract.getUserColors({"from":acc1})) == 0
    assert len(contract.getUserColors({"from":acc2})) == 0

    contract.mint(color_code_1,{"from":acc1})
    
    with pytest.raises(VirtualMachineError):
        contract.mint(color_code_1,{"from":acc1})

    with pytest.raises(VirtualMachineError):
        contract.mint(color_code_1,{"from":acc2})
    
    assert contract.colorExists(color_code_1) == True
    assert contract.colorExists(color_code_2) == False
    assert contract.colorExists(color_code_3) == False
    assert len(contract.getUserColors({"from":acc1})) == 1
    assert len(contract.getUserColors({"from":acc2})) == 0

    contract.mint(color_code_2,{"from":acc2})
    contract.mint(color_code_3,{"from":acc2})

    assert contract.colorExists(color_code_1) == True
    assert contract.colorExists(color_code_2) == True
    assert contract.colorExists(color_code_3) == True
    assert len(contract.getUserColors({"from":acc1})) == 1
    assert len(contract.getUserColors({"from":acc2})) == 2
