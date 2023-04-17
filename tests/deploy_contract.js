const ethers = require("ethers");
const ganache = require("ganache");
const fs = require("fs");

const contractFile = fs.readFileSync('build/contracts/SupplyChain.json');
const contract = JSON.parse(contractFile.toString());


const provider = new ethers.providers.Web3Provider(ganache.provider());
const ERC20_ABI = [
    "function addEntity(address _id, string memory _role) public"
]

const privateKey = "0x4d633117b6cc5572178c07ae35330570df896f1cfa91199309cc40d462349545"
const wallet = new ethers.Wallet(privateKey, provider);
const factory = new ethers.ContractFactory(contract.abi, contract.bytecode, wallet);

const main = async() => {
    const deployedContract = await factory.deploy();
    console.log("everything is ok, I guess");
}

main();