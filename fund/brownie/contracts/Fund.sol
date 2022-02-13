// SPDX-License-Identifier: MIT

pragma solidity 0.8.0;
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract Fund{
    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    address owner;
    address public topFunder;
    uint public count;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed){
        owner = msg.sender;
        priceFeed = AggregatorV3Interface(_priceFeed);
    }

    function getPrice() internal view returns(uint256){
      (,int256 price,,,) = priceFeed.latestRoundData();
      return uint256(price/10**8);
    }

    function getConversionRate(uint256 usdAmount)public view returns(uint256){
        uint256 ethPrice = getPrice();
        return (usdAmount * 10**8)/ethPrice;
    }

    function isOwner() public view returns(bool){
        return msg.sender == owner;
    }

    function fund() public payable {
        addressToAmountFunded[msg.sender]+=msg.value;
        funders.push(msg.sender);
        count++;
        if ( msg.sender != topFunder && addressToAmountFunded[msg.sender] >= addressToAmountFunded[topFunder] ){
            topFunder = msg.sender;
        }
    }

    modifier onlyOwner {
      require(msg.sender == owner);
      _;
    }

    function withdraw() public onlyOwner {
      payable(msg.sender).transfer(address(this).balance);
    }

    function currentFunds() public onlyOwner view returns(uint) {
        return address(this).balance;
    }
}