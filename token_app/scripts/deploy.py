from ape import accounts, project

def main():
    account = accounts.test_accounts[0]
    # contract = project.Token.deploy(sender=account)
    contract = account.deploy(project.MyToken, 1000000)
    print(f"Contract deployed at: {contract.address}")