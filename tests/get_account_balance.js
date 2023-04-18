const ethers = require("ethers");
const ganache = require("ganache");

const provider = new ethers.providers.Web3Provider(ganache.provider());

const ERC20_ABI = [
    "function addEntity(address _id, string memory _role) public"
]

const address = "0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0"
const contract = new ethers.Contract(address, ERC20_ABI, provider);

const main = async() => {
    const balance = await provider.getBalance(address);
    console.log(`\nETH Balance of ${address} --> ${ethers.utils.formatEther(balance)} ETH\n`);
}

main();
