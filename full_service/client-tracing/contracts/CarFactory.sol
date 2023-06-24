// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.19;

import "./Car.sol";

contract CarFactory {
    Car[] public cars;

    event CarCreated(Car _car);

    function createCar(
        uint64 _brand,
        uint64 _colour,
        string memory _ipfs_img
    ) external returns (Car car) {
        require(_brand <= uint64(Brand.MASERATI), "Invalid brand");
        require(_colour <= uint64(Colour.WHITE), "Invalid colour");
        
        Brand new_brand = Brand(_brand);
        Colour new_colour = Colour(_colour);
        car = new Car(new_brand, new_colour, _ipfs_img, msg.sender);
        cars.push(car);
        emit CarCreated(car);
    }
}
