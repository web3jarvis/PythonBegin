from ape import accounts
from ape.managers.project import LocalProject
import pathlib

ROOT = pathlib.Path(__file__).parent.parent.parent
project = LocalProject(ROOT)

CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"  

def get_contract():
    return project.Token.at(CONTRACT_ADDRESS)

def transfer_tokens(sender_id, recipient_address, amount):
    account = accounts.test_accounts[sender_id]
    contract = get_contract()
    tx_hash = contract.transfer(recipient_address, int(amount), sender=account)
    return tx_hash
