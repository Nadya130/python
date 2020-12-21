import datetime as datetime
from werkzeug.security import generate_password_hash

from app import Base, db

import enum


class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.INTEGER, autoincrement=True, primary_key=True)
    username = db.Column(db.VARCHAR(255), nullable=False)
    password = db.Column(db.VARCHAR(255), nullable=False)
    email = db.Column(db.VARCHAR(255), nullable=False)
    admin = db.Column(db.BOOLEAN, nullable=False)

    def __init__(self, username, password, email, admin):
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email
        self.admin = admin


class Bank(Base):
    __tablename__ = 'banks'
    id = db.Column(db.INTEGER, autoincrement=True, primary_key=True)
    name = db.Column(db.VARCHAR(255), nullable=False)
    budget = db.Column(db.BIGINT)


class Credit(Base):
    __tablename__ = 'credits'
    id = db.Column(db.INTEGER, autoincrement=True, primary_key=True)
    sum = db.Column(db.INT)
    status = db.Enum('unpaid', 'paid')
    userId = db.Column(db.INTEGER, db.ForeignKey(User.id))
   # user = db.relationship(User, backref='user')
    bankId = db.Column(db.INTEGER, db.ForeignKey(Bank.id))
    # bank = db.relationship(Bank, backref='bank')

    def __init__(self, sum, status, userId, bankId):
        self.sum = sum
        self.status = status
        self.userId = userId
        #self.user = user
        self.bankId = bankId
       # self.bank = bank


class StatusEnum(enum.Enum):
    unpaid = 'unpaid'
    paid = 'paid'
