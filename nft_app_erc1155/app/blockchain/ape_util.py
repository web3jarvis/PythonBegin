from ape import accounts, project

_contract_address = None

def get_contract(account):
    global _contract_address
    if not _contract_address:
        _contract_address = account.deploy(project.NFTMarketplace, account.address).address
    return project.NFTMarketplace.at(_contract_address)

def deploy_and_mint_nft(account_index, token_id, token_uri, nft_supply):
    account = accounts.test_accounts[account_index]
    nft_contract = get_contract(account)
    txn_receipt = nft_contract.mintNFT(account.address, token_id, nft_supply, token_uri, sender=account)
    return txn_receipt.txn_hash

def transfer_nft_owner(account_index, to_address, token_id, amount):
    account = accounts.test_accounts[account_index]
    nft_contract = get_contract(account)
    txn_receipt = nft_contract.transferNFT(account.address, to_address, token_id, amount, sender=account)
    return txn_receipt.txn_hash

def set_owner_royalty(account_index, recipient_address, fee_numerator):
    account = accounts.test_accounts[account_index]
    nft_contract = get_contract(account)
    txn_receipt = nft_contract.setRoyalty(recipient_address, fee_numerator, sender=account)
    return txn_receipt.txn_hash