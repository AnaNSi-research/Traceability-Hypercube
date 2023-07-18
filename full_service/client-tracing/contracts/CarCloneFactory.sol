// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "./Car.sol";
import "./CloneFactory.sol";
import "./Ownable.sol";

contract CarCloneFactory is Ownable, CloneFactory {
    address public libraryAddress;
    mapping (address => carInfo) carInfos;
    event CarCreated(carInfo _car_info);

    struct carInfo {
        Brand brand;
        Colour colour;
        address owner;
        string ipfs_img;
    }

    constructor(address _libraryAddress){
        libraryAddress = _libraryAddress;
    }

    function setLibraryAddress(address _libraryAddress) public onlyOwner {
        libraryAddress = _libraryAddress;
    }

    function createCar(Brand _brand, Colour _colour, string memory _ipfs_img) public onlyOwner {
        address car_addr = createClone(libraryAddress);
        Car car = Car(createClone(libraryAddress));
        car.init(_brand, _colour, _ipfs_img, msg.sender);
        carInfo memory car_info = carInfo(_brand, _colour, msg.sender, _ipfs_img);
        carInfos[car_addr] = car_info;
        emit CarCreated(car_info);
    }

    function getCarInfo(address _addr) public view returns (carInfo memory) {
        return carInfos[_addr];
    }
}