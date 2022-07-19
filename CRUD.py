from flask import make_response
import json
from check import *
from constraints import *


def db_connect():
    dataBase = pymysql.connect(
        host='39.103.183.155',  # MySQL服务端的IP地址
        port=3306,  # MySQL默认PORT地址(端口号)
        user='root',  # 用户名
        password='xx3721xx',  # 密码,也可以简写为passwd
        database='user',  # 库名称,也可以简写为db
        charset='utf8',  # 字符编码
        autocommit=True
    )
    return dataBase.cursor()


cur = db_connect()


# add user
def add_user(username, password, email, role):
    d = {'message': None,
         'cookies': '111',
         'token': 'abc'
         }
    status = '404'
    if password_check(password) and email_check(email):  # return false if email is already registered
        user = read_one(email)
        if user is None:
            cur.execute("insert into user_info(username, password, email, role) values (%s, %s, %s, %s)",
                        (username, password, email, role))
            cur.connection.commit()
            d['message'] = 'register successfully'
            d['user_info'] = user
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
        cur.execute("delete from user_info where email=%s", (email,))
        cur.connection.commit()
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
        if update_info['username']:
            cur.execute("update user_info set username=%s where email=%s",
                        (update_info['username'], email))
        if update_info['password']:
            cur.execute("update user_info set password=%s where email=%s",
                        (update_info['password'], email))
        if update_info['name']:
            cur.execute("update user_info set name=%s where email=%s",
                        (update_info['name'], email))
        if update_info['phone']:
            cur.execute("update user_info set phone=%s where email=%s",
                        (update_info['phone'], email))
        if update_info['age']:
            cur.execute("update user_info set age=%s where email=%s",
                        (int(update_info['age']), email))
        if 'role' in update_info.keys() and update_info['role']:
            cur.execute("update user_info set role=%s where email=%s",
                        (update_info['role'], email))
        cur.connection.commit()
        d["message"] = "Modify Successfully"
        status = '200'
    r = json.dumps(d)
    resp = make_response(r)
    resp.status = status
    return resp


# read one user info
def read_one(email, password=None):
    if password:
        cur.execute("select * from user_info where email=%s and password=%s", (email, password))
    else:
        cur.execute("select * from user_info where email=%s", (email,))
    info = cur.fetchone()
    return info


# read all user info
def read_all():
    cur.execute("select * from user_info")
    info = cur.fetchall()                       # get all users' data
    return info                                 # return tuple of user info dicts ({user1 info},{user2 info},{...})


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

