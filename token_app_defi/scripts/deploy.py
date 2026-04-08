from ape import accounts, project
from app.db import SessionLocal, Base, engine
from app.models import Token, AMM_Table
from datetime import datetime

def main():
    
    Base.metadata.create_all(bind=engine)
    db_session = SessionLocal()

    account = accounts.test_accounts[0]
    contractA = account.deploy(project.Token, "TokenA", "TOKA", 1000000)
    contractB = account.deploy(project.Token, "TokenB", "TOKB", 1000000)
    amm = account.deploy(project.AMM, contractA.address, contractB.address)

    contractA.approve(amm.address, 500000, sender=account)
    contractB.approve(amm.address, 500000, sender=account)
    amm.addLiquidity(500000, 500000, sender=account)
    
    new_token_a = Token(
        token_name="TokenA", token_symbol="TOKA",
        initial_supply=1000000, contract_address=contractA.address,
        owner_id=1
    )
    new_token_b = Token(
        token_name="TokenB", token_symbol="TOKB",
        initial_supply=1000000, contract_address=contractB.address,
        owner_id=1
    )
    new_amm = AMM_Table(
        amm_address=amm.address,
        token_a_address=contractA.address,
        token_b_address=contractB.address,
        timestamp=datetime.now()
    )
    db_session.add_all([new_token_a, new_token_b, new_amm])
    db_session.commit()
    db_session.close()

    print(f"TokenA:  {contractA.address}")
    print(f"TokenB:  {contractB.address}")
    print(f"AMM:     {amm.address}")