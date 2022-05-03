// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Lottery is VRFConsumerBase ,Ownable{
    address payable[] public players;
    uint256 public usdEntryFee; 
    uint256 public randomness;
    address public recentWinner;
    AggregatorV3Interface internal ethUsdPriceFedd;
    enum LOTTERY_STATE {
        OPEN,
        CLOSE,
        CALCULATING_WINER
    }

    LOTTERY_STATE public lottery_state;
    uint256 fee;
    bytes32 keyHash;


    constructor(address _priceFeedAddress, 
                address _vrfCoordinator, 
                uint256 _fee,
                address _link,
                bytes32 _keyHash
                ) 
    public VRFConsumerBase(_vrfCoordinator, _link) {
        usdEntryFee = 50 * (10 ** 18);
        ethUsdPriceFedd = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSE;
        fee = _fee;
        keyHash = _keyHash;
    }

    function enter() public payable {
        // 50$ minimum
        require(lottery_state == LOTTERY_STATE.OPEN, "the lottery is closed");
        require(msg.value >= getEntranceFee(), "Not enough ETH");
        players.push(msg.sender);
    }


    function getEntranceFee() public view returns(uint256){
        (,int256 answer,,,) = ethUsdPriceFedd.latestRoundData();
        uint256 adjuctedPrice = uint256(answer) * 10 **10; // 18 decimals  

        uint256 costToEnter = (usdEntryFee * 10 **18) / adjuctedPrice;
        return costToEnter;
    }

    function startLottery() public onlyOwner{
        require(lottery_state == LOTTERY_STATE.CLOSE, "can't start lottery yet.");
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner{
        lottery_state = LOTTERY_STATE.CALCULATING_WINER;
        requestRandomness(keyHash, fee);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness) internal override{
        require(lottery_state == LOTTERY_STATE.CALCULATING_WINER, "You are not there yet");
        require(_randomness > 0, "radnom-note-found");
        uint256 indexOfWinner = _randomness % players.length;
        recentWinner = players[indexOfWinner];
        recentWinner.transfer(address(this).balance);
        players = new address payable[](0);

        lottery_state = LOTTERY_STATE.CLOSE;
        randomness = _randomness;
    }
}