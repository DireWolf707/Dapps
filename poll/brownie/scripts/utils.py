import pathlib
from brownie import network,accounts,config
from brownie import Poll

def get_account():
    curr_net = network.show_active()
    if curr_net == 'development':
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["private_key"])

def export_contract(contract):
    path = pathlib.Path(__file__).parent.parent.parent
    path = path / "frontend" / "src"
    with open(path / "contract.js","w") as file:
        file.write(f"export let abi = {contract.abi};\n".replace("True","true").replace("False","false"))
        file.write(f"export let address = '{contract.address}';\n")
        file.write(f"export let pollAbi = {Poll.abi};".replace("True","true").replace("False","false"))