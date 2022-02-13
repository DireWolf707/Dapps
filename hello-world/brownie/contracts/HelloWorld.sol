// SPDX-License-Identifier: MIT
pragma solidity 0.8.0;

contract HelloWorld{
    string public data;

    event newData(string data);

    constructor(){
        data = "world";
    }

    function changeData(string memory _data) public {
        require(bytes(_data).length>0);
        data = _data;
        emit newData(_data);
    }
}