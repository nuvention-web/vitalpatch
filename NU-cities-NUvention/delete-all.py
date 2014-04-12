from cities import db
from cities import User

users = User.query.all()
for user in users:
    db.session.delete(user)
db.session.commit()