// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.19;

import "./Car.sol";
import "./CloneFactory.sol";
import "./Ownable.sol";

contract CarCloneFactory is Ownable, CloneFactory {
    address public baseCarAddress;
    Car[] public cars;
    event CarCreated(Car _car);

    constructor(address _baseCarAddress) {
        baseCarAddress = _baseCarAddress;
    }

    function setBaseCarAddress(address _baseCarAddress) public onlyOwner {
        baseCarAddress = _baseCarAddress;
    }

    function createCar(
        Brand _brand,
        Colour _colour,
        string memory _ipfs_img
    ) public onlyOwner returns (Car car) {
        car = Car(createClone(baseCarAddress));
        car.init(_brand, _colour, _ipfs_img, msg.sender);
        cars.push(car);
        emit CarCreated(car);
    }
}
