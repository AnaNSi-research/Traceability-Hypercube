// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "./Car.sol";
import "./CloneFactory.sol";

contract CarFactory is CloneFactory {
     Car[] public cars;
     address masterContract;

     constructor(address _masterContract){
         masterContract = _masterContract;
     }

     function createCar(uint data) external{
        Car car = Car(createClone(masterContract));
        car.init(data);
        cars.push(car);
     }

     function getCars() external view returns(Car[] memory){
         return cars;
     }
}