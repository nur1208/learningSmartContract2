from brownie import FundMe
from .helpful_scripts import get_account
def fund():
    fund_me = FundMe[-1]
    account = get_account()
    entrance_price = fund_me.getEntranceFee()

    print(f"The current entry fee is {entrance_price}")
    print("Funding")
    fund_me.fund( {"from":account, "value":entrance_price})

def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    fund_me.withdraw({"from":account})


def main():
    fund()
    withdraw()