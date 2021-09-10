from flask_login import UserMixin
from Parisodhan_Website import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id) #Int is used for avoiding any data error

class User(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    password=db.Column(db.String(60), nullable=False)   #hashed passwords will be absorbed
    
    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

db.create_all()


