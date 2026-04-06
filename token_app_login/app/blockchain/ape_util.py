from ape import accounts
from ape.managers.project import LocalProject
import pathlib

# __file__ gives the absolute path of this file (ape_util.py)
# .parent navigates one folder up: ape_util.py → blockchain/
# .parent.parent navigates two folders up: blockchain/ → app/
# .parent.parent.parent navigates three folders up: app/ → token_app/
# So ROOT = absolute path of token_app/ folder
ROOT = pathlib.Path(__file__).parent.parent.parent

# Tell Ape Framework that token_app/ is the root of our project
# Ape will now look for ape-config.yaml and contracts/ folder inside ROOT
# Without this, Ape gets confused about where Token.sol and its compiled ABI is
project = LocalProject(ROOT)

# This is the address where our Token contract was deployed on Anvil (local blockchain)
# Every time you redeploy, this address changes — update it here accordingly
# CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"  

def get_contract(contract_address):
    # project.Token → find the compiled Token.sol contract inside our project
    # .at(CONTRACT_ADDRESS) → go to this specific address on blockchain and return its object
    # This object lets us call functions defined in Token.sol like transfer() and balanceOf()
    return project.Token.at(contract_address)

def transfer_tokens(sender_id, recipient_address, amount, contract_address):
    # accounts.test_accounts is a list of 10 fake wallets that Anvil provides automatically
    # sender_id is an integer index (0, 1, 2...) — we pick the wallet at that position
    # Example: sender_id=0 gives the first Anvil wallet, sender_id=1 gives the second
    account = accounts.test_accounts[sender_id]
    
    # Call get_contract() to get the deployed Token contract object
    # We need this object to call the transfer() function defined in Token.sol
    contract = get_contract(contract_address)
    
    # Call the transfer() function from Token.sol with three arguments:
    # recipient_address → wallet address of the person receiving the tokens
    # int(amount) → number of tokens to send (converted to integer because Solidity expects uint256)
    # sender=account → tells Ape which wallet should sign this transaction (like a digital signature)
    # The return value tx_hash is a unique ID that Ethereum gives to every transaction
    # transfer() also waits for the transaction to be mined and included in a block, so when we get the tx_receipt back, we know the transaction is complete.
    tx_receipt = contract.transfer(recipient_address, int(amount), sender=account)
    
    # Send the transaction ID back to app.py
    # app.py will store this tx_hash in the database as proof that the transaction happened
    return tx_receipt.tx_hash

def deploy_token(owner_id, token_name, token_symbol, initial_supply):
    # accounts.test_accounts is a list of 10 fake wallets that Anvil provides automatically
    # owner_id is an integer index (0, 1, 2...) — we pick the wallet at that position to be the token owner
    # Example: owner_id=0 gives the first Anvil wallet, owner_id=1 gives the second
    # The token owner is the one who deploys the contract and receives the initial supply of tokens in their wallet.
    # We need to specify the token owner because the constructor of our Token contract in Token.sol assigns the initial supply to the deployer's address.
    # So if we want the initial supply to go to a specific wallet, that wallet must be the one that deploys the contract.
    # If we didn't specify the owner and just used accounts.test_accounts[0] by default, then the first Anvil wallet would always be the token owner, which might not be what we want in a multi-user app.
    # By allowing the user to choose the owner_id, we can have different users deploy their own tokens and receive the initial supply in their respective wallets.
    # This also makes the app more flexible and realistic, as in a real-world scenario, different people would deploy their own tokens and be the initial holders of those tokens.
    # In summary, specifying the owner_id allows us to control which wallet becomes the token owner and receives the initial supply, making our app more dynamic and user-friendly.
    # ----------------------------------------------------------------------
    account = accounts.test_accounts[owner_id]  # token owner account
    # ----------------------------------------------------------------------
    # Deploy the Token contract to the blockchain with the constructor arguments:
    # token_name, token_symbol, initial_supply. The deploy() function returns the deployed contract object.
    # The deploy() function also takes care of sending the deployment transaction and waiting for it to be mined.
    # After deployment, the contract object contains the address where the contract is deployed, which we can return to app.py.
    # Note: Every time you deploy, a new contract is created at a new address. So we return the new address after deployment.
    # ----------------------------------------------------------------------
    #deploy() also takes a sender argument to specify which wallet is deploying the contract. This is important because the deployer becomes the token owner and receives the initial supply of tokens in their wallet. 
    contract = account.deploy(project.Token, token_name, token_symbol, initial_supply)
    return contract.address  # ← new contract_address return after deployment
