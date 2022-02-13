import time,pytest
from scripts.deploy import deploy
from brownie import Poll,Voting,accounts
from brownie.exceptions import VirtualMachineError

Poll1="my poll"
Poll2="my poll 2"
Options=["a","b"]

def test_deploy():
    assert len(Voting) == 0
    deploy()
    assert len(Voting) == 1

def test_voting():
    voting = Voting[-1]
    acc1=accounts[0]
    acc2=accounts[1]

    assert voting.isOwner({"from":acc1}) == True
    assert voting.isOwner({"from":acc2}) == False

    assert len(voting.getPolls()) == 0

    with pytest.raises(VirtualMachineError):
        voting.createPoll(Poll1,Options,{"from":acc2})
    with pytest.raises(VirtualMachineError):
        voting.createPoll("",Options,{"from":acc1})
    with pytest.raises(VirtualMachineError):
        voting.createPoll(Poll1,["a"],{"from":acc1})

    voting.createPoll(Poll1,Options,{"from":acc1})
    voting.createPoll(Poll2,Options,{"from":acc1})

    assert len(voting.getPolls()) == 2

def test_polls():
    voting = Voting[-1]
    acc1=accounts[0]
    acc2=accounts[1]

    polls = voting.getPolls()
    poll1 = Poll.at(polls[0])
    poll2 = Poll.at(polls[1])

    assert poll1.name() == Poll1
    assert poll2.name() == Poll2

    assert poll1.voted(acc1) == False
    assert poll2.voted(acc1) == False

    options = poll1.getOptions()
    for i in range(len(options)):
        assert options[i][0] == Options[i]

    with pytest.raises(VirtualMachineError):
        poll1.vote(2,{"from":acc1})
    
    with pytest.raises(OverflowError):
        poll1.vote(-1,{"from":acc1}) 

    poll1.vote(0,{"from":acc1}) 

    assert poll1.options(0)[1] == 1
    assert poll1.options(1)[1] == 0

    with pytest.raises(VirtualMachineError):
        poll1.vote(0,{"from":acc1})

    poll1.vote(0,{"from":acc2}) 

    assert poll1.options(0)[1] == 2
    assert poll1.options(1)[1] == 0

    time.sleep(1)



