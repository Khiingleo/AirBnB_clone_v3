#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user", cascade='delete')
        reviews = relationship("Review", backref="user", cascade='delete')
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        if kwargs:
            password = kwargs.pop('password', None)
            if password:
                User.hash_password(self, password)
        super().__init__(*args, **kwargs)

    def hash_password(self, password):
        """ hashes a password """
        hashed_object = hashlib.md5()
        hashed_object.update(password.encode("utf-8"))
        hashed_password = hashed_object.hexdigest()
        setattr(self, "password", hashed_password)
