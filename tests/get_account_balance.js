const ethers = require("ethers");
const ganache = require("ganache");

const url = "http://localhost:8545"

const provider = new ethers.providers.JsonRpcProvider(url);

const ERC20_ABI = [
    "function addEntity(address _id, string memory _role) public"
]

const address = "0x9060dA808374b7579565017b3c9baB8778606d7d"
const contract = new ethers.Contract(address, ERC20_ABI, provider);

const main = async() => {
    const balance = await provider.getBalance(address);
    console.log(`\nETH Balance of ${address} --> ${ethers.utils.formatEther(balance)} ETH\n`);
}

main();
