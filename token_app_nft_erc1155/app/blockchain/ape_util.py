from ape import accounts, project

_contract_address = None

def get_contract(account):
    global _contract_address
    
    if _contract_address is None:
        deployed_contract = account.deploy(project.MyCustomNFT, account.address)
        _contract_address = deployed_contract.address
        return deployed_contract
    
    return project.MyCustomNFT.at(_contract_address)

def deploy_and_mint_nft(account_index, token_id, token_uri):
    account = accounts.test_accounts[account_index]
    nft_contract = get_contract(account)
    txn_receipt = nft_contract.mintNFT(account.address, token_id, 1, token_uri, sender=account)
    return txn_receipt.txn_hash

def transfer_nft_owner(account_index, to_address, token_id, amount):
    account = accounts.test_accounts[account_index]
    nft_contract = get_contract(account)
    txn_receipt = nft_contract.transferNFT(account.address, to_address, token_id, amount, sender=account)
    return txn_receipt.txn_hash