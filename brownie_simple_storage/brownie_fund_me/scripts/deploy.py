from brownie import FundMe, network, config, MockV3Aggregator
from .helpful_scripts import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS

def deploy_fund_me():
    account = get_account()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_fund_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    
    else:
        deploy_mocks()
        price_fund_address = MockV3Aggregator[-1].address

    fundMe = FundMe.deploy(price_fund_address,{"from":account},publish_source=config["networks"][network.show_active()].get("verify"))
    print(f"Contract deployed to {fundMe.address}")

    return fundMe

def main():
    deploy_fund_me()