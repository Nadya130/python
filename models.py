from app import Base, db


class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.INTEGER, autoincrement=True, primary_key=True)
    username = db.Column(db.VARCHAR(255), nullable=False)
    firstName = db.Column(db.VARCHAR(255), nullable=False)
    lastName = db.Column(db.VARCHAR(255), nullable=False)
    password = db.Column(db.VARCHAR(255), nullable=False)
    phoneNumber = db.Column(db.VARCHAR(20), nullable=False)

class Bank(Base):
    __tablename__ = 'banks'
    id = db.Column(db.INTEGER, autoincrement=True, primary_key=True)
    name = db.Column(db.VARCHAR(255), nullable=False)
    budget = db.Column(db.BIGINT)

class Credit(Base):
    __tablename__ = 'credits'
    id = db.Column(db.INTEGER, autoincrement=True, primary_key=True)
    sum = db.Column(db.INT)
    datetime = db.Column(db.DATETIME)
    status = db.Enum('unpaid', 'payed')
    userId = db.Column(db.INTEGER, db.ForeignKey(User.id))
    user = db.relationship(User, backref='user')
    bankId = db.Column(db.INTEGER, db.ForeignKey(Bank.id))
    bank = db.relationship(Bank, backref='bank')
