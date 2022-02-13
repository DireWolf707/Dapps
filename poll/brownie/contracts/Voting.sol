// SPDX-License-Identifier: MIT

pragma solidity 0.8.0;


contract Poll{
    string public name;
    uint public totalVotes;

    struct Option{
        string name;
        uint count;
    }

    Option[] public options;

    mapping(address => bool) public voted;

    constructor(string memory _name,string[] memory _options){
        require(bytes(_name).length > 0,"Length of poll name is 0");
        require(_options.length >= 2,"Atleast two options!");

        name = _name;
        for (uint256 i = 0; i < _options.length; i++) {
            options.push(Option(_options[i],0));
        }
    }

    function vote(uint _optionId) public {
        require(_optionId < options.length,"Wrong vote Id!");
        require(!voted[msg.sender],"Already voted!");
        voted[msg.sender]=true;

        options[_optionId].count++;
        totalVotes++;
    }

    function getOptions() public view returns(Option[] memory) {
        return options;
    }
}

contract Voting{
    address owner;
    Poll[] public polls;
    
    constructor(){
        owner=msg.sender;
    }

    function isOwner() public view returns(bool){
        return owner==msg.sender;
    }

    function createPoll(string memory _name,string[] memory _options) public {
        require(isOwner());
        Poll poll = new Poll(_name,_options);
        polls.push(poll);
    }

    function getPolls()public view returns(Poll[] memory){
        return polls;
    }
}