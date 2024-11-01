from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True)
    # hashed passwd
    password = Column(String(60), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_flagged = Column(Boolean, default=False)

class ContactForm(Base):
    __tablename__ = 'contactforms'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False)
    message = Column(String(500), nullable=False)
