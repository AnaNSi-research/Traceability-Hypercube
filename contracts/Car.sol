// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract Car {
    string public colour;
    string public brand;

    // use this function instead of the constructor
    // since creation will be done using createClone() function
    function init(string memory _brand, string memory _colour) external {
        brand = _brand;
        colour = _colour;
    }

    function getColour() external view returns(string memory){
        return colour;
    }

    function getBrand() external view returns(string memory){
        return brand;
    }
}
