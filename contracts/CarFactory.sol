// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "./Car.sol";
import "../node_modules/@optionality.io/clone-factory/contracts/CloneFactory.sol";
import "../node_modules/@openzeppelin/contracts/access/Ownable.sol";

contract CarFactory is Ownable, CloneFactory {
    string[] private colours = ["rosso", "giallo", "blu", "nero", "bianco"];
    string[] private brands = ["ferrari", "lamborghini"];
    address public libraryAddress;

    struct carInfo {
        string brand;
        string colour;
    }

    mapping(address => carInfo) public carInfos;

    event CarCreated(address newCarAddress);

    constructor(address _libraryAddress){
        libraryAddress = _libraryAddress;
    }

    function setLibraryAddress(address _libraryAddress) public onlyOwner {
        libraryAddress = _libraryAddress;
    }

    function createCar(string memory brand, string memory colour) external {
        require(checkBrand(brand), "Brand not available, pick another");
        require(checkColour(colour), "Colour not available, pick another");

        address car = createClone(libraryAddress);
        Car(car).init(brand, colour);
        addCarInfo(car, carInfo(brand, colour));
        emit CarCreated(car);
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

    function addCarInfo(address _addr, carInfo memory car_info) public {
        carInfos[_addr] = car_info;
    }

    function getCarInfo(address _addr) public view returns(carInfo memory) {
        return carInfos[_addr];
    }
}