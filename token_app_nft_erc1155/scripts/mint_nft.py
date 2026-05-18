from ape import accounts, project

def main():
    
    owner = accounts.test_accounts[0]
    recipient = accounts.test_accounts[1]

    print("🚀 Deploying MyCustomNFT contract...")
    
    nft_contract = owner.deploy(project.MyCustomNFT, owner.address)
    print(f"✅ Contract deployed at: {nft_contract.address}\n")

    metadata_uri = "ipfs://bafkreidq3mfl5s3w6n465nyq57kguoo62fm7hjodqf3ubml7odpktnxj2q"
    
    token_name = "My Custom NFT Pass"

    print(f"🎨 Minting NFT to address {recipient.address}...")
    
    tx = nft_contract.mintNFT(recipient.address, metadata_uri, token_name, sender=owner)
    
    print("\n🎉 NFT Minted Successfully!")
    print(f"Transaction hash: {tx.txn_hash}")