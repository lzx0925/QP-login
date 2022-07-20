from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:xx3721xx@39.103.183.155/user"

db.init_app(app)


class User(db.Model):
    __tablename__ = 'user_info'
    uid = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    phone = db.Column(db.Integer)


    def __init__(self, password, email, username, role, name=None, age=None, phone=None):
        self.password = password
        self.email = email
        self.username = username
        self.role = role
        self.name = name
        self.age = age
        self.phone = phone

    def __repr__(self):
        return '<User %r>' % self.email

if __name__ == "__main__":
    app.run()
