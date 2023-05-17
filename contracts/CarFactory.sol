// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/proxy/Clones.sol";
import "./Car.sol";

contract CarFactory {
    //Creating an array of car addresses
    Car[] public CarAddresses;
    address public implementationAddress;
    event carAdded(Car car, string message);

    function addCar() public {
      //Creating a new crew object, you need to pay //for the deployment of this contract everytime - $$$$
      Car carAddress =  Car(Clones.clone(implementationAddress));

      // since the clone create a proxy, the constructor is redundant and you have to use the initialize function
      carAddress.initialize(); 

      //Adding the new crew to our list of crew addresses
      CarAddresses.push(carAddress);
      emit carAdded(carAddress, "Car added!");
  }
}