from ape import accounts, project

def deploy_and_mint_nft(account_index, token_uri, token_name):
    account = accounts.test_accounts[account_index]
    nft_contract = account.deploy(project.MyCustomNFT, account.address)
    txn_receipt = nft_contract.mintNFT(account.address, token_uri, token_name, sender=account)
    return txn_receipt.txn_hash