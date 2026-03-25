from ape import accounts, project

def main():
    account = accounts.test_accounts[0]
    contract = account.deploy(project.Token, 1000000)
    print(f"Contract deployed at: {contract.address}")