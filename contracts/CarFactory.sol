// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "./Car.sol";
import "./CloneFactory.sol";

contract CarFactory is CloneFactory {
    Car[] public cars;

    string[] private colours = ["rosso", "giallo", "blu", "nero", "bianco"];
    string[] private brands = ["ferrari", "lamborghini"];
    address masterContract;

    constructor(address _masterContract){
        masterContract = _masterContract;
    }

    function createCar(string memory brand, string memory colour) external{

        require(checkBrand(brand), "Brand not available, pick another");
        require(checkColour(colour), "Colour not available, pick another");
        Car car = Car(createClone(masterContract));
        car.init(brand, colour);
        cars.push(car);
    }

    function getCars() external view returns(Car[] memory){
        return cars;
    }

    function checkColour(string memory colour) private view returns(bool) {
        for(uint i = 0; i < colours.length; i++) {
            if (compareStrings(colours[i], colour)) {
                return true;
            }
        }
        return false;
    }

    function checkBrand(string memory brand) private view returns(bool) {
        for(uint i = 0; i < brands.length; i++) {
            if (compareStrings(brands[i], brand)) {
                return true;
            }
        }
        return false;
    }

    function compareStrings(string memory a, string memory b) private pure returns(bool) {
        return (keccak256(abi.encodePacked((a))) == keccak256(abi.encodePacked((b))));
    }
}