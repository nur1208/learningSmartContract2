from brownie import FundMe, network, config
from .helpful_scripts import get_account

def deploy_fund_me():
    account = get_account()
    # 0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
    if network.show_active() != "development":
        price_fund_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    fundMe = FundMe.deploy(price_fund_address,{"from":account},publish_source=True)
    print(f"Contract deployed to {fundMe.address}")
    

def main():
    deploy_fund_me()