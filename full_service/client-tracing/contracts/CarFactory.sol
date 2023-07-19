// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "./Car.sol";

contract CarFactory {
    Car[] public cars;

    event CarCreated(Car _car);

    function createCar(
        Brand _brand,
        Colour _colour,
        string memory _ipfs_img
    ) external returns (Car car) {
        car = new Car(_brand, _colour, _ipfs_img, msg.sender);
        cars.push(car);
        emit CarCreated(car);
    }
}
