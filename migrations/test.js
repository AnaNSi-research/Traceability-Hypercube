const ethers = require("ethers");
const ganache = require("ganache");


const provider = new ethers.providers.Web3Provider(ganache.provider());
const address = "0x9060dA808374b7579565017b3c9baB8778606d7d"
const main = async() => {
    const balance = await provider.getBalance(address);
    console.log(`\nETH Balance of ${address} --> ${ethers.utils.formatEther(balance)} ETH\n`);
}

main();
