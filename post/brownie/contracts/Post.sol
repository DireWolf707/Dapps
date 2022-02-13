// SPDX-License-Identifier: MIT

pragma solidity 0.8.0;
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract Posts{
    struct Post {
        string title;
        string content;
        uint tip;
        address author;
    }

    Post[] public posts;

    AggregatorV3Interface priceFeed;

    constructor(address _priceFeedAddress) {
        priceFeed = AggregatorV3Interface(_priceFeedAddress);
    }

    function getPosts()public view returns(Post[] memory){
        return posts;
    }

    function createPost(string memory _title, string memory _content) public {
        require(bytes(_title).length > 0 && bytes(_content).length > 0 );
        posts.push(Post(_title,_content,0,msg.sender));
    }

    function updatePost(string memory _title, string memory _content,uint _id) public {
        require(bytes(_title).length > 0 && bytes(_content).length > 0 && _id < posts.length );
        Post storage _post = posts[_id];
        require(_post.author == msg.sender);
        _post.title = _title;
        _post.content = _content;
    }

    function tipPost(uint _id) public payable{
        require(_id < posts.length);
        Post storage _post = posts[_id];
        require(_post.author != msg.sender);
        payable(_post.author).transfer(msg.value);
        _post.tip += msg.value;
    }

    function getPrice() internal view returns(uint256){
      (,int256 price,,,) = priceFeed.latestRoundData();
      return uint256(price/10**8);
    }

    function getConversionRate(uint256 usdAmount)public view returns(uint256){
        uint256 ethPrice = getPrice();
        return (usdAmount * 10**8)/ethPrice;
    }
}