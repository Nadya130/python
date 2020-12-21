from models import *
from datetime import datetime
db.create_all()

# user = User(username='user1', password='1', email='1@gmail.com', admin=True)
# user2 = User(username='user2', password='2', email='2@gmail.com', admin=False)
# bank = Bank(name='BestBank', budget=517000)
credit = Credit(sum=5100, userId=1, bankId=1, status='unpaid')


# db.session.add(user)
# db.session.add(user2)
# db.session.add(bank)
db.session.add(credit)

db.session.commit()
