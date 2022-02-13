import pytest,time
from brownie import network,Lottery
from scripts.utils import LOCAL_NETWORKS,fund_with_link, get_account
from scripts.deploy import deploy


def test_can_pick_winner():
    if network.show_active() in LOCAL_NETWORKS:
        pytest.skip()
    deploy()
    lottery = Lottery[-1]
    owner = get_account()
    lottery.startLottery({"from":owner})
    lottery.enter({"from":owner,"value":lottery.getEntranceFee()})
    lottery.enter({"from":owner,"value":lottery.getEntranceFee()})
    fund_with_link(lottery.address)
    lottery.endLottery({"from":owner})  
    time.sleep(60*3)
    assert lottery.lastWinner()==owner.address
    assert lottery.balance() == 0