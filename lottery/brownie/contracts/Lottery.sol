// SPDX-License-Identifier: MIT

pragma solidity 0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract Lottery is VRFConsumerBase, Ownable {
    address[] public players;
    address public lastWinner;
    uint public usdEntryFee;
    mapping(address => bool) public playerEntered;

    enum LOTTERY_STATE {OPEN, CLOSED, CALCULATING_WINNER }
    LOTTERY_STATE public lottery_state;

    AggregatorV3Interface public priceFeed;

    bytes32 internal keyHash;
    uint256 internal fee;

    event RequestRandomness(bytes32 requestId);

    constructor(
        address _priceFeed,
        address _vrf,
        address _link,
        bytes32 _keyHash,
        uint256 _fee
    ) VRFConsumerBase(_vrf, _link) {
        usdEntryFee = 50;
        priceFeed = AggregatorV3Interface(_priceFeed);
        lottery_state = LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyHash = _keyHash;
    }

    function getPlayers() public view returns(address[] memory) {
        return players;
    }

    function isOwner() public view returns(bool) {
        return owner()==msg.sender;
    }

    function enter() public payable{
        require(lottery_state == LOTTERY_STATE.OPEN);
        require(!isOwner());
        require(!playerEntered[msg.sender]);
        require(msg.value >= (getEntranceFee()),"Not enough ETH!");
        playerEntered[msg.sender]=true;
        players.push(msg.sender); 
    }

    function getPrice() public view returns(uint){
      (,int256 price,,,) = priceFeed.latestRoundData();
      return uint(price);
    }

    function getEntranceFee() public view returns(uint) {
        uint ethPrice = getPrice();
        return (usdEntryFee * 10**18 * 10**8)/ethPrice ;
    }
    
    function startLottery() public onlyOwner {
        require(lottery_state == LOTTERY_STATE.CLOSED,"Can't start a new lottery yet!");
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        require(LINK.balanceOf(address(this)) >= fee, "Not enough LINK - fill contract with faucet");
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        bytes32 requestId = requestRandomness(keyHash,fee);
        emit RequestRandomness(requestId);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness) internal override {
        require(lottery_state == LOTTERY_STATE.CALCULATING_WINNER,"Can't fulfill Randomness yet!");
        require(_randomness>0,"random not found");
        lastWinner = players[_randomness % players.length];
        payable(lastWinner).transfer(address(this).balance);
        // Reset
        for (uint256 i = 0; i < players.length; i++) {
            delete playerEntered[players[i]];
        }
        players = new address[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
    }
}