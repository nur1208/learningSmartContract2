// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";
// we don't need save math with solidity > 0.8.0
contract FundMe{
    // safe math library check uint256 for integer overflows
    using SafeMathChainlink for uint256;

    mapping(address => uint256) public addressToAmountFund;
    address public owner;
    address[] public funders;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) public{
        priceFeed = AggregatorV3Interface(_priceFeed);
        // msg whoever deploy this smartcontract
        owner = msg.sender;
    }

    function fund() public payable{ 
        uint256 minimumUSD = 50 * 10 ** 18;
        require(getConversionRate(msg.value)  >= minimumUSD, "You need to spend more ETH!");
        addressToAmountFund[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns(uint256){
        return priceFeed.version();
    }

    function getDecimals() public view returns(uint8){
        return priceFeed.decimals();
    }



    function getPrice() public view returns(uint256){
        (,int256 answer,,,) = priceFeed.latestRoundData();
        // ETH/USD rate in 18 digit
        // answer will be in 8 digit
        // so then add 10 more digit to equle 18.
        // converting to Wei
        return uint256(answer * 10000000000);
    }

    
    // function getEnterancePrice() public view returns(uint256){
    //     uint256 minimumUSD = 50 * 10 ** 18;
    //     uint256 price = getPrice();
    //     uint256 precistion = 1 * 10**18;
    //     return ((minimumUSD * precistion) / price) + 1;
    // }

    function getEntranceFee() public view returns (uint256) {
        // minimumUSD
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        // return (minimumUSD * precision) / price;
        // We fixed a rounding error found in the video by adding one!
        return ((minimumUSD * precision) / price) + 1;
    }
    function getConversionRate(uint256 ethAmount) public view returns(uint256){
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        return ethAmountInUsd;
    }

    modifier onlyOwner {
        // first run the code then require
        // _;
        require(msg.sender == owner, "you not the owner of this contract");
        // first run require  then run reset of the code
        _;
    } 


    function withdraw() onlyOwner public payable {
        // If you are using version eight (v0.8) of chainlink aggregator interface,
        // you will need to change the code below to
        // payable(msg.sender).transfer(address(this).balance);

        // require(msg.sender == owner, "you not the owner of this contract");
        msg.sender.transfer(address(this).balance);

        for(uint256 index=0; index < funders.length; index++ ){
            address funder = funders[index];
            addressToAmountFund[funder] = 0;
        }

        funders = new address[](0);

    }


}
