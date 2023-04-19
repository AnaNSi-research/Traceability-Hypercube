const ethers = require("ethers");

const url = "http://localhost:8545"
const provider = new ethers.providers.JsonRpcProvider(url);

// private key of the account that was used to deploy the smart contract
const privateKey = "0x4d633117b6cc5572178c07ae35330570df896f1cfa91199309cc40d462349545"
const wallet = new ethers.Wallet(privateKey, provider);

const ERC20_ABI = [
    "function addEntity(address _id, string memory _role) public",
    "event AddEntity(address entityId, string entityRole)"
]
const address = "0x792c2a0EBD62A74Bd02F51bbA4e6233bB58D45b2";
const contract = new ethers.Contract(address, ERC20_ABI, provider);

const main = async() => {
    const contractWithWallet = contract.connect(wallet);
    const accounts = await provider.listAccounts();

    const roleEnum = {
        ISSUER: {val: "ISSUER", pos: 0},
        PROVER: {val: "PROVER", pos: 1},
        VERIFIER: {val: "VERIFIER", pos: 2}
    };

    const statusEnum = {
        MANUFACTURED: {val: "MANUFACTURED", pos: 0},
        DELIVERING1: {val: "DELIVERING_INTERNATIONAL", pos: 1},
        STORED: {val: "STORED", pos: 2},
        DELIVERING2: {val: "DELIVERING_LOCAL", pos: 3},
        DELIVERED: {val: "DELIVERED", pos: 4}
    };

    const entity = {id: accounts[1], role: roleEnum.ISSUER.val};

    await contractWithWallet.addEntity(entity.id, entity.role);

    const addEntityEvents = await contract.queryFilter("AddEntity");
    console.log(addEntityEvents);
    
}

main();