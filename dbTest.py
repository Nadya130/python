from models import *
from datetime import datetime
db.create_all()

user = User(username='nadya', firstName='Nadiia', lastName='Horishna', password='root', phoneNumber='065333')
credit = Credit(sum=5100, datetime=datetime(2019, 11, 11), userId=1, bankId=1)
bank = Bank(name='Avowal', budget=517000)
user1 = User(username='aaa', firstName='A', lastName='B', password='root', phoneNumber='0676755333')


db.session.add(user)
db.session.add(user1)

db.session.add(credit)
db.session.add(bank)
db.session.commit()
