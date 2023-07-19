// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

enum Colour {RED, YELLOW, BLUE, BLACK, WHITE}
enum Brand {FERRARI, LAMBORGHINI, MASERATI}

contract Car {
    Colour public colour;
    Brand public brand;
    address public owner;
    string public ipfs_img;

    function init(Brand _brand, Colour _colour, string memory _ipfs_img, address _owner) external {
        brand = _brand;
        colour = _colour;
        ipfs_img = _ipfs_img;
        owner = _owner;
    }
    
    constructor(Brand _brand, Colour _colour, string memory _ipfs_img, address _owner) {
        brand = _brand;
        colour = _colour;
        ipfs_img = _ipfs_img;
        owner = _owner;
    }
}