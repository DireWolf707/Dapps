// SPDX-License-Identifier: MIT

pragma solidity 0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract ColorNFT is ERC721{

    mapping(string => bool) public colorExists;
    mapping(address => string[]) userColors;
    uint tokenId;

    constructor() ERC721("Color","COLOR"){}

    function mint(string memory _color) public {
        require(!colorExists[_color]);
        _mint(msg.sender,tokenId);
        tokenId++;
        colorExists[_color] = true;
        userColors[msg.sender].push(_color);
    }

    function getUserColors() public view returns(string[] memory) {
        return userColors[msg.sender];
    }
}