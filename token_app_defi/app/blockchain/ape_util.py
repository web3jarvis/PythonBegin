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

def deploy_amm(owner_id, tokenA_address, tokenB_address):
    account = accounts.test_accounts[owner_id]  # AMM owner account
    amm = account.deploy(project.AMM, tokenA_address, tokenB_address)
    return amm.address

def get_amm_contract(amm_address):
    return project.AMM.at(amm_address)

def add_liquidity(sender_id, amm_address, amountA, amountB):
    account = accounts.test_accounts[sender_id]
    project.Token.at(get_amm_contract(amm_address).tokenA()).approve(amm_address, int(amountA), sender=account)
    project.Token.at(get_amm_contract(amm_address).tokenB()).approve(amm_address, int(amountB), sender=account)
    amm = get_amm_contract(amm_address)
    tx_receipt = amm.addLiquidity(int(amountA), int(amountB), sender=account)
    return tx_receipt.tx_hash

def swap_tokens(sender_id, amm_address, from_token, amount):
    account = accounts.test_accounts[sender_id]
    amm = get_amm_contract(amm_address)
    if from_token == 'A':
        project.Token.at(amm.tokenA()).approve(amm_address, int(amount), sender=account)
        tx_receipt = amm.swapAForB(int(amount), sender=account)
    else:
        project.Token.at(amm.tokenB()).approve(amm_address, int(amount), sender=account)
        tx_receipt = amm.swapBForA(int(amount), sender=account)
    return tx_receipt.tx_hash