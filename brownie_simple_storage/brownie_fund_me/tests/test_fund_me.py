from scripts.deploy import deploy_fund_me
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from brownie import network , accounts, exceptions
import pytest

def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_price = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from": account, "value": entrance_price})
    tx.wait(1)
    print(account)
    assert fund_me.addressToAmountFund(account.address) == entrance_price
    tx2 = fund_me.withdraw({"from":account})
    tx2.wait(1)
    assert fund_me.addressToAmountFund(account.address) == 0

def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")

    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
    # tx1.wait(1)

