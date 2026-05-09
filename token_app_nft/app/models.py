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
    tx_type         = Column(String, nullable=False, default='transfer')
    tx_hash         = Column(String, unique=True, index=True, nullable=False)
    timestamp       = Column(DateTime, default=datetime.now)
    
    # ---------------------------   Relationships with User and Token -------------------------
    sender          = relationship("User", foreign_keys=[sender_id], back_populates="sent_tx")
    receiver        = relationship("User", foreign_keys=[receiver_id], back_populates="received_tx")

class NFTCollection(Base):
    __tablename__   = "nft_collection_table"
    
    id              = Column(Integer, primary_key=True, index=True)
    owner_id        = Column(Integer, ForeignKey("user_table.id"))
    name            = Column(String, nullable=False)
    description     = Column(String, nullable=True)
    image_cid       = Column(String, nullable=True)
    metadata_uri    = Column(String, nullable=True)
    timestamp       = Column(DateTime, default=datetime.now)
    
    owner           = relationship("User", backref="nft_collections")