from ape import accounts
from ape.managers.project import LocalProject
import pathlib

ROOT = pathlib.Path(__file__).parent.parent.parent
project = LocalProject(ROOT)

def get_contract(contract_address):
    return project.Token.at(contract_address)

def transfer_tokens(sender_id, recipient_address, amount, contract_address):
    account = accounts.test_accounts[sender_id]
    contract = get_contract(contract_address)
    tx_receipt = contract.transfer(recipient_address, int(amount), sender=account)
    return tx_receipt.tx_hash

def deploy_token(owner_id, token_name, token_symbol, initial_supply):
    account = accounts.test_accounts[owner_id]  # token owner account
    contract = account.deploy(project.Token, token_name, token_symbol, initial_supply)
    return contract.address  # ← new contract_address return after deployment
