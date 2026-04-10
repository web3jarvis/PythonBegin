from ape import accounts, project
from db import SessionLocal, Base, engine
from models import AMM_Table, Token

def main():
    Base.metadata.create_all(bind=engine)
    db_session = SessionLocal()

    # ── Wipe stale records so unique constraints don't conflict ──
    db_session.query(AMM_Table).delete()
    db_session.query(Token).filter(Token.token_name.in_(["TokenA", "TokenB"])).delete()
    db_session.commit()

    account   = accounts.test_accounts[0]
    contractA = account.deploy(project.Token, "TokenA", "TOKA", 1000000)
    contractB = account.deploy(project.Token, "TokenB", "TOKB", 1000000)
    amm       = account.deploy(project.AMM, contractA.address, contractB.address)

    contractA.approve(amm.address, 500000, sender=account)
    contractB.approve(amm.address, 500000, sender=account)
    amm.addLiquidity(500000, 500000, sender=account)

    db_session.add_all([
        Token(token_name="TokenA", token_symbol="TOKA",
              initial_supply=1000000, contract_address=contractA.address, owner_id=1),
        Token(token_name="TokenB", token_symbol="TOKB",
              initial_supply=1000000, contract_address=contractB.address, owner_id=1),
        AMM_Table(amm_address=amm.address,
                  token_a_address=contractA.address,
                  token_b_address=contractB.address)
    ])
    db_session.commit()
    db_session.close()

    print(f"✅ TokenA: {contractA.address}")
    print(f"✅ TokenB: {contractB.address}")
    print(f"✅ AMM:    {amm.address}")