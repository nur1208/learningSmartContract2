import json, os
from solcx import compile_standard,  install_solc
from web3 import Web3 
from dotenv import load_dotenv
# import request

# print("here")
# res=request.get("http://127.0.0.1:8545/")

# print(res)
load_dotenv()
with open("./contracts/SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

print("Installing...")
install_solc('0.6.0')
#compile Our Solidity

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]

# For connecting to ganache
# w3 = Web3(Web3.HTTPProvider(endpoint_uri="http://127.0.0.1:8545",
# request_kwargs={'timeout': 600}))
w3 = Web3(Web3.HTTPProvider('https://rinkeby.infura.io/v3/1dd7a7de09ab4e90826e1c6defc7d3aa'))

chain_id = 4
my_address = "0x33Ce94f3DC8d07ce41a46B197d79ff08F4BFA6D0"
private_key = os.getenv("PRIVATE_KEY")

# Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi,bytecode=bytecode)

# Get the latest transaction nonce
nonce = w3.eth.getTransactionCount(my_address)

# Build the transaction that deploys the contract
print(w3.eth.gas_price * 2)
transaction = SimpleStorage.constructor().buildTransaction(
    
{ "gasPrice": w3.eth.gas_price  ,"chainId":chain_id, "from":my_address, "nonce":nonce}
)

# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

print("Deploying Contract!")
# Send it!
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Done! Contract deployed to {tx_receipt.contractAddress}")


# Working with deployed Contracts
simpleStorage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

print(f"Initial Stored Value {simpleStorage.functions.retrieve().call()}")
# print(simpleStorage.functions.store(55).call())
# print(simpleStorage.functions.retrieve().call())

store_transaction = simpleStorage.functions.store(55).buildTransaction(
    {"gasPrice": w3.eth.gas_price  ,"chainId": chain_id, "from":my_address, "nonce": nonce + 1}
)

signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
store_transaction_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
print("Updating stored Value...")
tx_receipt = w3.eth.wait_for_transaction_receipt(store_transaction_hash)


print(simpleStorage.functions.retrieve().call())
