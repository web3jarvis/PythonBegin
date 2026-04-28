# --------------------------- Imports -------------------------
from db import Base
from sqlalchemy import Boolean, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from flask_login import UserMixin

# --------------------------- User Model -------------------------
class User(UserMixin, Base):
    __tablename__   = "user_table"
    
    id              = Column(Integer, primary_key=True, index=True)
    username        = Column(String, unique=True, index=True)
    password        = Column(String, nullable=False)
    is_admin        = Column(Boolean, default=False)
    timestamp       = Column(DateTime, default=datetime.now)
    
    wallet          = relationship("Wallet", backref="owner", lazy=True)
    tokens          = relationship("Token", back_populates="owner")
    pools           = relationship("AMM", back_populates="poolcreator")
    sent_tx         = relationship("Transaction", foreign_keys="[Transaction.sender_id]", back_populates="sender")
    received_tx     = relationship("Transaction", foreign_keys="[Transaction.receiver_id]", back_populates="receiver")
    
class Wallet(Base):
    __tablename__   = "wallet_table"
    
    id              = Column(Integer, primary_key=True, index=True)
    wallet_address  = Column(String, unique=True, index=True)
    public_key      = Column(String, unique=True, index=True)
    wallet_ownerid  = Column(Integer, ForeignKey("user_table.id"))
    timestamp       = Column(DateTime, default=datetime.now)

class Transaction(Base):
    __tablename__   = "transaction_table"

    id              = Column(Integer, primary_key=True, index=True)
    sender_id       = Column(Integer, ForeignKey("user_table.id"))
    receiver_id     = Column(Integer, ForeignKey("user_table.id"))
    amount          = Column(Float, nullable=False)
    tx_type         = Column(String, nullable=False, default='transfer')  # 'transfer' or 'swap'
    tx_hash         = Column(String, unique=True, index=True, nullable=False)
    token_id        = Column(Integer, ForeignKey("token_table.id"))
    received_amount = Column(Float)  # to be used for swap transactions to record how much of the other token was received
    received_token_id = Column(Integer, ForeignKey("token_table.id"))  # to be used for swap transactions to record which token was received
    timestamp       = Column(DateTime, default=datetime.now)
    
    # ---------------------------   Relationships with User and Token -------------------------
    sender          = relationship("User", foreign_keys=[sender_id], back_populates="sent_tx")
    receiver        = relationship("User", foreign_keys=[receiver_id], back_populates="received_tx")
    token           = relationship("Token", foreign_keys=[token_id], back_populates="transactions")
    received_token  = relationship("Token", foreign_keys=[received_token_id])
    
class Token(Base):
    __tablename__   = "token_table"
    
    id              = Column(Integer, primary_key=True, index=True)
    token_name      = Column(String, unique=True, index=True)
    token_symbol    = Column(String, unique=True, index=True)
    initial_supply  = Column(Float, nullable=False)
    contract_address = Column(String, unique=True, index=True, nullable=False)
    token_ownerid   = Column(Integer, ForeignKey("user_table.id"))
    is_stake_active = Column(Boolean, default=False)
    staking_address = Column(String, unique=True, index=True, nullable=True)
    timestamp       = Column(DateTime, default=datetime.now)
    
    owner           = relationship("User", back_populates="tokens")
    transactions    = relationship("Transaction", foreign_keys=[Transaction.token_id], back_populates="token")
    amm_token_A     = relationship("AMM", foreign_keys="[AMM.token_A_address]", back_populates="token_A")
    amm_token_B     = relationship("AMM", foreign_keys="[AMM.token_B_address]", back_populates="token_B")
    
class AMM(Base):
    __tablename__ = "amm_table"
    
    id                  = Column(Integer, primary_key=True, index=True)
    amm_address         = Column(String, unique=True, index=True)
    token_A_address     = Column(String, ForeignKey("token_table.contract_address"), nullable=False)
    token_B_address     = Column(String, ForeignKey("token_table.contract_address"), nullable=False)
    reserve_A           = Column(Float, nullable=False, default=0.0)
    reserve_B           = Column(Float, nullable=False, default=0.0)
    initial_reserve_A   = Column(Float, nullable=False, default=0.0)
    initial_reserve_B   = Column(Float, nullable=False, default=0.0)
    amm_txn_hash        = Column(String, unique=True, index=True, nullable=False)
    amm_ownerid         = Column(Integer, ForeignKey("user_table.id"))
    timestamp           = Column(DateTime, default=datetime.now)
    
    token_A             = relationship("Token", foreign_keys=[token_A_address], back_populates="amm_token_A")
    token_B             = relationship("Token", foreign_keys=[token_B_address], back_populates="amm_token_B")
    poolcreator         = relationship("User", foreign_keys=[amm_ownerid], back_populates="pools")