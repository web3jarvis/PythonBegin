# --------------------------- Imports -------------------------
from db import Base
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from flask_login import UserMixin




# --------------------------- User Model -------------------------
class User(UserMixin, Base):
    __tablename__   = "users"

    id              = Column(Integer, primary_key=True, index=True)
    username        = Column(String, unique=True, index=True)
    password        = Column(String, nullable=False)
    timestamp       = Column(DateTime, default=datetime.now)
    
    # ---------------------------   Relationships with Token, Transaction, and Wallet -------------------------
    tokens          = relationship("Token", back_populates="owner")
    sent_tx         = relationship("Transaction", foreign_keys="Transaction.sender_id", back_populates="sender")
    received_tx     = relationship("Transaction", foreign_keys="Transaction.recipient_id", back_populates="recipient")
    user_wallets    = relationship("Wallet", backref="owner", lazy=True)




# --------------------------- Transaction Model -------------------------
class Transaction(Base):
    __tablename__   = "transactions"

    id              = Column(Integer, primary_key=True, index=True)
    sender_id       = Column(Integer, ForeignKey("users.id"))
    recipient_id    = Column(Integer, ForeignKey("users.id"))
    amount          = Column(Float, nullable=False)
    tx_hash         = Column(String, unique=True, index=True, nullable=False)
    token_id        = Column(Integer, ForeignKey("tokens.id"))
    timestamp       = Column(DateTime, default=datetime.now)
    
    # ---------------------------   Relationships with User and Token -------------------------
    sender          = relationship("User", foreign_keys=[sender_id], back_populates="sent_tx")
    recipient       = relationship("User", foreign_keys=[recipient_id], back_populates="received_tx")
    token           = relationship("Token", back_populates="transactions")
    
    
    
    
# --------------------------- Token Model -------------------------
class Token(Base):
    __tablename__   = "tokens"

    id              = Column(Integer, primary_key=True, index=True)
    token_name      = Column(String, unique=True, index=True)
    token_symbol    = Column(String, unique=True, index=True)
    initial_supply  = Column(Float, nullable=False)
    contract_address = Column(String, unique=True, index=True, nullable=False)
    owner_id        = Column(Integer, ForeignKey("users.id"))
    token_timestamp = Column(DateTime, default=datetime.now)
    
    # ---------------------------   Relationships with User and Transaction -------------------------
    owner           = relationship("User", back_populates="tokens")
    transactions    = relationship("Transaction", back_populates="token")




# --------------------------- Wallet Model -------------------------    
class Wallet(Base):
    __tablename__   = "wallets"

    id              = Column(Integer, primary_key=True, index=True)
    wallet_address  = Column(String, unique=True, index=True)
    public_key      = Column(String, unique=True, index=True)
    timestamp       = Column(DateTime, default=datetime.now)
    user_wallet     = Column(Integer, ForeignKey("users.id"))
    

class AMM_Table(Base):
    __tablename__ = "amms"
    
    id                  = Column(Integer, primary_key=True, index=True)
    amm_address         = Column(String, unique=True, index=True)
    token_a_address     = Column(String, nullable=False)
    token_b_address     = Column(String, nullable=False)
    timestamp           = Column(DateTime, default=datetime.now)