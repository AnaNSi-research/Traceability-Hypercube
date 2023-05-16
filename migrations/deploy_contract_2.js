const ethers = require("ethers");
const fs = require("fs");

const contractFile = fs.readFileSync('build/contracts/Car.json');
const contract = JSON.parse(contractFile.toString());


const url = "http://localhost:8545"
const provider = new ethers.providers.JsonRpcProvider(url);

const ERC20_ABI = [
    "function sayHello() public pure returns (string memory)"
]

const privateKey = "0x4d633117b6cc5572178c07ae35330570df896f1cfa91199309cc40d462349545"
const wallet = new ethers.Wallet(privateKey, provider);
const factory = new ethers.ContractFactory(contract.abi, contract.bytecode, wallet);

const main = async() => {
    const deployedContract = await factory.deploy();
    console.log(`Deployed contract with address: ${deployedContract.address}`);
}

main();