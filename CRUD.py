from flask import make_response
import json
from constraints import *
from config import *
import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from user_db_class import *

#db = SQLAlchemy()

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:xx3721xx@39.103.183.155/user"


db.init_app(app)
with app.app_context():
    db.create_all()


def db_connect():
    dataBase = pymysql.connect(
        host=HOST,  # MySQL服务端的IP地址
        port=PORT,  # MySQL默认PORT地址(端口号)
        user=USERNAME,  # 用户名
        password=PASSWORD,  # 密码,也可以简写为passwd
        database=DATABASE,  # 库名称,也可以简写为db
        charset='utf8',  # 字符编码
        autocommit=True
    )
    return dataBase.cursor()


cur = db_connect()


# add user
def add_user(username, password, email, role, name=None, age=None, phone=None):
    d = {'message': None,
         'cookies': '111',
         'token': 'abc'
         }
    status = '404'
    if password_check(password) and email_check(email):  # return false if email is already registered
        exist = read_one(email)
        if exist is None:
            user = User(password, email, username, role, name, age, phone)
            db.session.add(user)
            db.session.commit()
            d['message'] = 'register successfully'
            d['email'] = email
            status = '200'
        else:
            d['message'] = 'email already exists'
    else:
        d['message'] = 'invalid email or password'
    r = json.dumps(d)
    resp = make_response(r)
    resp.status = status
    return resp


# delete user
def delete(email):
    d = {'email': email,
         'cookies': '111',
         'token': 'abc'
         }
    status = '404'
    if read_one(email) is None:  # if cannot find email in database
        d['message'] = 'Delete failed, cannot find email'
    else:  # if find email in database, delete it
        query = User.query.filter_by(email=email).one()
        db.session.delete(query)
        db.session.commit()
        d['message'] = 'Delete Successfully'
        status = '200'
    r = json.dumps(d)
    resp = make_response(r)
    resp.status = status
    return resp


# update user
def update(email, update_info):
    d = {
        "Modified_email": email,
        'cookies': '111',
        'token': 'abc'
        }
    status = '404'
    if not read_one(email):  # return false if cannot find email in database
        d["message"] = "Modify failed. Error: Email Doesn't Exist"
    elif update_info['password'] and not password_check(update_info['password']):  # return error message to page if password voilates rules
        d["message"] = "Modify failed. Error: Invalid Password"
    else:  # else update data
        query = User.query.filter_by(email=email).first()
        if update_info['username']:
            query.username=update_info['username']
        if update_info['password']:
            query.password = update_info['password']
        if update_info['name']:
            query.name = update_info['name']
        if update_info['phone']:
            query.phone = int(update_info['phone'])
        if update_info['age']:
            query.age = int(update_info['age'])
        if 'role' in update_info.keys() and update_info['role']:
            query.role = update_info['role']
        db.session.commit()
        d["message"] = "Modify Successfully"
        status = '200'
    r = json.dumps(d)
    resp = make_response(r)
    resp.status = status
    return resp


# read one user info
def read_one(email, password=None):
    if password:
        query = User.query.filter_by(email=email, password=password).first()
    else:
        query = User.query.filter_by(email=email).first()
    return [query.uid, query.password, query.email, query.username, query.role, query.name, query.age, query.phone]


def login(email, password):
    d = {
        'message': None,
        'email': email,
        'role': None,
        'cookies': '111',
        'token': 'abc'
    }
    status = '404'
    if password_check(password) and email_check(email):
        info = read_one(email,password)
        if info:
            d['message'] = 'user login successfully'
            d['user_info'] = info
            d['role'] = info[4]
            status = '200'
        else:
            d['message'] = 'login failed, error: pswd and email not match'
    else:
        d['message'] = 'Invalid password or email'
    r = json.dumps(d)
    resp = make_response(r)
    resp.status = status
    return resp

if __name__ == "__main__":
    app.run()