from brownie import Contract, accounts, config, network, MockV3Aggregator

FORK_ENVIRONMENTS = ["mainnet-fork"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

def get_account(index=None, id=None):
    if index:
        return accounts[index]

    if id:
        return accounts.load(id)

    if(network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORK_ENVIRONMENTS):
        return accounts[0]


    return accounts.add(config["wallets"]["from_key"])

contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator
}

def get_contract(contract_name):
    """This function will grab the contract addresses from the brownie config
        if defined, otherwise, it will deploy a mock version of that contract, and
        return that mock contract.
        Args:
            contract_name (string)
        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed
            version of this contract.
    """
    contract_type = contract_to_mock[contract_name]
    if (network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS):
        if(len(contract_type) <= 0):
            deploy_mocks()
            contract_type.deploy()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_type]
        contract = Contract.from_abi(contract_type._name, )

    return contract
DECIMALS = 8
INITAIL_VALUE = 200000000000

def deploy_mocks(decimals=DECIMALS, initial_value=INITAIL_VALUE):
    account = get_account()
    mock_feed_feed = MockV3Aggregator.deploy(decimals, initial_value
        {"from": account})
    print("Deployed!")
