// SPDX-License-Identifier: MIT

pragma solidity 0.8.0;

contract TodoList{

    struct Task{
        string content;
        bool completed;
    }
    
    mapping(address => Task[]) tasks;

    function createTask(string memory _content) public {
        tasks[msg.sender].push(Task(_content,false));
    }

    function getTasks() public view returns(Task[] memory) {
        return tasks[msg.sender];
    }

    function changeCompleted(uint _id) public {
        Task storage _task = tasks[msg.sender][_id];
        _task.completed = !_task.completed;
    }

    function changeContent(uint _id,string memory content) public {
        Task storage _task = tasks[msg.sender][_id];
        _task.content = content;
    }
}