from ape import accounts
from ape import project
from ape.contracts import ContractInstance
from ape.types import ContractType
import pathlib, json

ROOT = pathlib.Path("C:/PythonBegin/token_app_defi")

def _load_contract(name, address):

    artifact_path =ROOT / ".build" / "__local__.json"
    with artifact_path.open() as f:
        contract_data = json.load(f)
        contract_type = contract_data.get("contractTypes",{}).get(name)
        final_contract_type = ContractType.model_validate(contract_type)
        print(f"Loaded contract type for {name}: {final_contract_type}")
    return ContractInstance(contract_type=final_contract_type, address=address)
    
    # artifact_path = ROOT / ".build" / "__local__.json"
    # with open(artifact_path) as f:
    #     contract_type = ContractType.model_validate(json.load(f))
    # return ContractInstance(address, contract_type)

def get_contract(contract_address):
    return _load_contract("Token", contract_address)

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
    return _load_contract("AMM", amm_address)

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