from ape import accounts, project
from ape.contracts import ContractInstance
from ape.types import ContractType
import pathlib, json

ROOT = pathlib.Path("C:/PythonBegin/token_app_custom_defi")

# --------------------------------------------- Helper functions ---------------------------------------------
def _load_contract(name, address):

    artifact_path = ROOT / ".build" / "__local__.json"
    with artifact_path.open() as f:
        contract_data = json.load(f)
        contract_type = contract_data.get("contractTypes",{}).get(name)
        final_contract_type = ContractType.model_validate(contract_type)
        print(f"Loaded contract type for {name}: {final_contract_type}")
    return ContractInstance(contract_type=final_contract_type, address=address)

# --------------------------------------------- Token related functions ---------------------------------------------
def get_contract(contract_address):
    return _load_contract("Token", contract_address)

def deploy_token(owner_id, token_name, token_symbol, initial_supply):
    account = accounts.test_accounts[owner_id]  # token owner account  
    contract = account.deploy(project.Token, token_name, token_symbol, initial_supply)
    tx_receipt = contract.creation_metadata.receipt
    return contract.address, tx_receipt.txn_hash

def transfer_tokens(sender_id, receiver_address, amount, contract_address):
    account = accounts.test_accounts[sender_id]
    token_contract = get_contract(contract_address)
    tx_receipt = token_contract.transfer(receiver_address, amount * (10**18), sender=account)
    return tx_receipt.txn_hash

# --------------------------------------------- AMM related functions ---------------------------------------------
def get_amm_contract(amm_pool_address):
    return _load_contract("AMMPool", amm_pool_address)

def deploy_pool(owner_id, tokenA_address, tokenB_address):
    account = accounts.test_accounts[owner_id]  # AMM owner account
    amm_pool = account.deploy(project.AMMPool, tokenA_address, tokenB_address)
    return amm_pool.address

def add_liquidity(sender_id, amm_pool_address, amountA, amountB):
    account = accounts.test_accounts[sender_id]
    project.Token.at(get_amm_contract(amm_pool_address).tokenA()).approve(amm_pool_address, int(amountA) * (10**18), sender=account)
    project.Token.at(get_amm_contract(amm_pool_address).tokenB()).approve(amm_pool_address, int(amountB) * (10**18), sender=account)
    amm_pool = get_amm_contract(amm_pool_address)
    tx_receipt = amm_pool.addLiquidity(int(amountA) * (10**18), int(amountB) * (10**18), sender=account)
    return tx_receipt.txn_hash

def swap_tokens(sender_id, amm_pool_address, from_token, amount):
    account = accounts.test_accounts[sender_id]
    amm_pool = get_amm_contract(amm_pool_address)
    if from_token == 'A':
        project.Token.at(amm_pool.tokenA()).approve(amm_pool_address, int(amount) * (10**18), sender=account)
        tx_receipt = amm_pool.swapAforB(int(amount * (10**18)), sender=account)
    else:
        project.Token.at(amm_pool.tokenB()).approve(amm_pool_address, int(amount) * (10**18), sender=account)
        tx_receipt = amm_pool.swapBforA(int(amount * (10**18)), sender=account)
    return tx_receipt.txn_hash

# --------------------------------------------- Staking related functions ---------------------------------------------
def get_staking_contract(staking_address):
    return _load_contract("Staking", staking_address)

def deploy_staking(token_address):
    account = accounts.test_accounts[0]  # Staking contract owner account
    staking_contract = account.deploy(project.Staking, token_address)
    return staking_contract.address

def execute_stake(sender_id, token_address, staking_address, amount):
    account = accounts.test_accounts[sender_id]
    token_contract = get_contract(token_address)
    staking_contract = get_staking_contract(staking_address)
    token_contract.approve(staking_address, int(amount), sender=account)
    tx_receipt = staking_contract.stake(int(amount), sender=account)
    return tx_receipt.txn_hash

def execute_unstake(sender_id, token_address, staking_address, amount):
    account = accounts.test_accounts[sender_id]
    token_contract = get_contract(token_address)
    staking_contract = get_staking_contract(staking_address)
    tx_receipt = staking_contract.unstake(int(amount), sender=account)
    return tx_receipt.txn_hash
