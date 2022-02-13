import pathlib
from brownie import network,accounts,config,MockV3Aggregator,MockVRFCoordinator,LinkToken,Contract

TESTING_NETWORKS = ("development","mainnet-fork","mainnet-fork-dev")
LOCAL_NETWORKS = ("development","ganache-local")

def get_account(account_idx=None):
    if account_idx:
        return accounts[account_idx]
    curr_net = network.show_active()
    if curr_net in TESTING_NETWORKS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["private_key"])

def export_contract(contract):
    path = pathlib.Path(__file__).parent.parent.parent
    path = path / "frontend" / "src"
    with open(path / "contract.js","w") as file:
        file.write(f"export let abi = {contract.abi};".replace("True","true").replace("False","false"))
        file.write(f"export let address = '{contract.address}';")

contract_to_mock = {
    "eth_usd_price_feed":MockV3Aggregator,
    "vrf":MockVRFCoordinator,
    "link":LinkToken,
}

def deploy_mocks(decimals=8,initial_value=3000*10**8):
    account = get_account()
    MockV3Aggregator.deploy(decimals,initial_value,{"from":account})
    link_token = LinkToken.deploy({"from":account})
    MockVRFCoordinator.deploy(link_token.address,{"from":account})

def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]

    curr_network = network.show_active()
    if curr_network in LOCAL_NETWORKS:
        if len(contract_type) <= 0:
            print("deploying mocks!")
            deploy_mocks()
            print("Mocks deployed!")
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][curr_network][contract_name]
        contract = contract_type.at(contract_address)
        #contract = Contract.from_abi(contract_type._name,contract_address,contract_type.abi)
    return contract

def fund_with_link(contract_address,account=None,link_token=None,amount=0.1*10**18):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link")
    tx = link_token.transfer(contract_address,amount,{"from":account})
    tx.wait(1)
    print("LINK FUNDED")