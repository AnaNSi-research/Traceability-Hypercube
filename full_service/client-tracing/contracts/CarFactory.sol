// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.19;

import "./Car.sol";

contract CarFactory {
    Car[] public cars;

     function createCar(string memory _brand, string memory _colour, string memory _ipfs_img) external returns(Car car) {
        car = new Car(_brand, _colour, _ipfs_img, msg.sender);
        cars.push(car);
    }
}