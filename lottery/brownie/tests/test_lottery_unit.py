import pytest
from brownie import Lottery,MockVRFCoordinator,accounts,network
from brownie.exceptions import VirtualMachineError
from scripts.deploy import deploy
from scripts.utils import LOCAL_NETWORKS,fund_with_link

def test_deploy():
    assert len(Lottery) == 0
    deploy()
    assert len(Lottery) == 1

def test_get_entrance_fee():
    if network.show_active() not in LOCAL_NETWORKS:
        pytest.skip()
    lottery = Lottery[-1]
    acc1 = accounts[0]
    assert (lottery.getEntranceFee()) == ((50 * 10**18 * 10**8)/(3000*10**8))

def test_cant_enter_until_started():
    if network.show_active() not in LOCAL_NETWORKS:
        pytest.skip()
    lottery = Lottery[-1]
    acc = accounts[1]
    with pytest.raises(VirtualMachineError):
        lottery.enter({"from":acc,"value":lottery.getEntranceFee()})

def test_start_lottery():
    if network.show_active() not in LOCAL_NETWORKS:
        pytest.skip()
    lottery = Lottery[-1]
    acc1 = accounts[0]
    acc2 = accounts[1]

    with pytest.raises(VirtualMachineError):
        lottery.startLottery({"from":acc2})
    
    lottery.startLottery({"from":acc1})

def test_can_enter_when_started():
    if network.show_active() not in LOCAL_NETWORKS:
        pytest.skip()
    lottery = Lottery[-1]
    acc1 = accounts[1]
    acc2 = accounts[2]
    acc3 = accounts[3]

    with pytest.raises(VirtualMachineError):
        lottery.enter({"from":acc1,"value":lottery.getEntranceFee()-10**6})

    lottery.enter({"from":acc1,"value":lottery.getEntranceFee()})
    assert lottery.players(0) == acc1.address
    lottery.enter({"from":acc2,"value":lottery.getEntranceFee()})
    lottery.enter({"from":acc3,"value":lottery.getEntranceFee()})

def test_end_lottery():
    if network.show_active() not in LOCAL_NETWORKS:
        pytest.skip()
    lottery = Lottery[-1]
    owner = accounts[0]
    acc3 = accounts[3]
    
    with pytest.raises(VirtualMachineError):
        lottery.endLottery({"from":owner})
    
    fund_with_link(lottery.address)

    with pytest.raises(VirtualMachineError):
        lottery.endLottery({"from":acc3})

    tx = lottery.endLottery({"from":owner})
    assert lottery.lottery_state() == 2

    request_id = tx.events["RequestRandomness"]["requestId"]
    random_number = 779 # %3 = 2 (3rd account)
    prev_balance = acc3.balance()
    lottery_amount = lottery.balance()

    vrf = MockVRFCoordinator[-1]
    vrf.callBackWithRandomness(request_id,random_number,lottery.address,{"from":owner})

    assert lottery.lastWinner() ==  acc3.address
    assert lottery.balance() == 0
    assert prev_balance + lottery_amount == acc3.balance()