from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# user has username and a list of environments
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True)

    # Define the relationship to Environment
    # User can have many environments
    environments = relationship("Environment", back_populates="users")

    # totp 
    is_totp_enabled = Column(Boolean, default=False)
    totp_secret = Column(String(50))


# environment has machine name, course and ip address
class ContactForm(Base):
    __tablename__ = 'contactforms'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False)
    message = Column(String(500), nullable=False)

    users = relationship("User", back_populates="environments")
    user_id = Column(Integer, ForeignKey('users.id'))
    
