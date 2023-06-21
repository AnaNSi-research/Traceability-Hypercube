// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.19;

contract Car {
    string public colour;
    string public brand;
    address public owner;
    string public ipfs_img;

    constructor(string memory _brand, string memory _colour, string memory _ipfs_img, address _owner) {
        brand = _brand;
        colour = _colour;
        ipfs_img = _ipfs_img;
        owner = _owner;
    }
}