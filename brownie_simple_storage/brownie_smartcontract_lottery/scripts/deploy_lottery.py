
from .helpful_scripts import get_account
from brownie import Lottery

def deploy_lottery():
    account = get_account(id="nur")
    print("working")
    pass

def main():
    deploy_lottery()