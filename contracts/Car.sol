// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;
import "@openzeppelin/contracts/access/Ownable.sol";

contract Car is Ownable {
    address public car;

    function initialize() public {
        require(car == address(0), "already initialized");
        car = msg.sender;
    }

    function sayHello() public pure returns (string memory) {
        return "Hello World!";
    }
}
