from ape import accounts, project

def deploy_and_mint_nft(account_index, token_id, token_uri):
    account = accounts.test_accounts[account_index]
    nft_contract = account.deploy(project.MyCustomNFT, account.address)
    txn_receipt = nft_contract.mintNFT(account.address, token_id, 1, token_uri, sender=account)
    return txn_receipt.txn_hash

def transfer_nft_owner(account_index, to_address, token_id, amount):
    account = accounts.test_accounts[account_index]
    nft_contract = account.deploy(project.MyCustomNFT, account.address)
    txn_receipt = nft_contract.transferNFT(to_address, token_id, amount, sender=account)
    return txn_receipt.txn_hash