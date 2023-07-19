// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "./Car.sol";
import "./CloneFactory.sol";
import "./Ownable.sol";

contract CarCloneFactory is Ownable, CloneFactory {
    address public baseCarAddress;
    // mapping (address => carInfo) carInfos;
    Car[] public cars;
    // event CarCreated(carInfo _car_info);
    event CarCreated(Car _car);

    // struct carInfo {
    //     Brand brand;
    //     Colour colour;
    //     address owner;
    //     string ipfs_img;
    // }

    constructor(address _baseCarAddress){
        baseCarAddress = _baseCarAddress;
    }

    function setLibraryAddress(address _baseCarAddress) public onlyOwner {
        baseCarAddress = _baseCarAddress;
    }

    function createCar(Brand _brand, Colour _colour, string memory _ipfs_img) public onlyOwner {
        // address car_addr = createClone(baseCarAddress);
        Car car = Car(createClone(baseCarAddress));
        car.init(_brand, _colour, _ipfs_img, msg.sender);
        // carInfo memory car_info = carInfo(_brand, _colour, msg.sender, _ipfs_img);
        // carInfos[car_addr] = car_info;
        // emit CarCreated(car_info);
        cars.push(car);
        emit CarCreated(car);
    }

    // function getCarInfo(address _addr) public view returns (carInfo memory) {
    //     return carInfos[_addr];
    // }
}