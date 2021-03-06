pragma solidity ^0.6.0;

contract SimpleStorage {
    // favoriteNumber by default eqauls 0
    uint256 public favoriteNumber; 

    struct People {
        uint256 favoriteNumber;
        string name;
    }

    People[] public people; 
    mapping(string => uint256) public nameToFavoriteNumber;

    function store(uint256 _favoriteNumber) public returns(uint256){
        favoriteNumber = _favoriteNumber;
        return favoriteNumber;
    }

    function retrieve() public view returns(uint256){
        return favoriteNumber;
    }

    function addPeople(string memory _name, uint256 _favoriteNumber) public{
        people.push(People(_favoriteNumber, _name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
 
}