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
CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"  

def get_contract():
    # project.Token → find the compiled Token.sol contract inside our project
    # .at(CONTRACT_ADDRESS) → go to this specific address on blockchain and return its object
    # This object lets us call functions defined in Token.sol like transfer() and balanceOf()
    return project.Token.at(CONTRACT_ADDRESS)

def transfer_tokens(sender_id, recipient_address, amount):
    # accounts.test_accounts is a list of 10 fake wallets that Anvil provides automatically
    # sender_id is an integer index (0, 1, 2...) — we pick the wallet at that position
    # Example: sender_id=0 gives the first Anvil wallet, sender_id=1 gives the second
    account = accounts.test_accounts[sender_id]
    
    # Call get_contract() to get the deployed Token contract object
    # We need this object to call the transfer() function defined in Token.sol
    contract = get_contract()
    
    # Call the transfer() function from Token.sol with three arguments:
    # recipient_address → wallet address of the person receiving the tokens
    # int(amount) → number of tokens to send (converted to integer because Solidity expects uint256)
    # sender=account → tells Ape which wallet should sign this transaction (like a digital signature)
    # The return value tx_hash is a unique ID that Ethereum gives to every transaction
    tx_hash = contract.transfer(recipient_address, int(amount), sender=account)
    
    # Send the transaction ID back to app.py
    # app.py will store this tx_hash in the database as proof that the transaction happened
    return tx_hash