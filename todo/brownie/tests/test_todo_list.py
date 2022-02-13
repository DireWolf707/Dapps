from pickle import FALSE
from brownie import TodoList,accounts
from scripts.deploy import deploy
import time

def test_deploy():
    assert len(TodoList) == 0
    deploy()
    assert len(TodoList) == 1

def test_todo():
    contract = TodoList[-1]
    content_idx = 0
    complted_idx = 1
    acc1 = accounts[0]
    acc2 = accounts[1]
    task1 = "task#1"
    task2 = "task#2"
    task3 = "task#3"

    assert len(contract.getTasks({"from":acc1})) == 0
    contract.createTask(task1,{"from":acc1})
    assert len(contract.getTasks({"from":acc1})) == 1

    assert len(contract.getTasks({"from":acc2})) == 0
    contract.createTask(task1,{"from":acc2})
    contract.createTask(task2,{"from":acc2})
    assert len(contract.getTasks({"from":acc2})) == 2

    task_id = 0

    assert contract.getTasks({"from":acc2})[task_id][complted_idx] == False
    contract.changeCompleted(task_id,{"from":acc2})
    assert contract.getTasks({"from":acc2})[task_id][complted_idx] == True

    assert contract.getTasks({"from":acc2})[task_id][content_idx] == task1
    contract.changeContent(task_id,task3,{"from":acc2})
    assert contract.getTasks({"from":acc2})[task_id][content_idx] == task3

    time.sleep(1)



