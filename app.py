# Author: Zixin Li
from flask import Flask, render_template, request, url_for, make_response
from flask_mysqldb import MySQL
from werkzeug.utils import redirect
import json
# from requests import *
import pymysql




app = Flask(__name__)
'''
app.config['MYSQL_HOST'] = '39.103.183.155'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'xx3721xx'
app.config['MYSQL_DB'] = 'user'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
'''
def sqlshow(res):
    for i in res:
        print(i)

def cont_sql(input_ip='39.103.183.155', input_port=3306, input_user='root', input_passwd='xx3721xx', inpout_databasename='user'):
    # 链接服务端
    try:
        dataBase = pymysql.connect(
            host    = input_ip,                      # MySQL服务端的IP地址
            port    = input_port,                    # MySQL默认PORT地址(端口号)
            user    = input_user,                    # 用户名
            password= input_passwd,                  # 密码,也可以简写为passwd
            database= inpout_databasename,           # 库名称,也可以简写为db
            charset = 'utf8',                        # 字符编码
            autocommit = True
        )
        cursor = dataBase.cursor()
        print("sucessfully connected!")
        print(type(cursor))
    except Exception as err:
        print(err)
        print(err)
        print('error!')
    # 貌似没有什么显示
    cursor.execute("USE event_zt;")
    print('cursor.execute("USE user;")')
    sqlshow(cursor)
    cursor.execute("SHOW TABLES;")
    print('cursor.execute("SHOW TABLES;")')
    sqlshow(cursor)


@app.route('/', methods=['GET', 'POST'])
def user_register():
    if request.method == "POST":
        info = request.json
        print(info)
        return add_user(info['username'], info['password'], info['email'], 'User')


@app.route('/admin_add', methods=['GET', 'POST'])
def admin_add():
    if request.method == "POST":
        info = request.json
        print(info)
        return add_user(info['username'], info['password'], info['email'], info['role'])


def add_user(username, password, email, role):
    d = {'message': None,
         'cookies': '111',
         'token': 'abc'
         }
    if not password_check(password) or not email_check(email):  # return error message to page if email or password voilates rules
        d['message'] = 'invalid email or password'
        r = json.dumps(d)
        resp = make_response(r)
        resp.status = '404'
        return resp
    if check_unique(email):                                                     # return false if email is already registered
        #cur = mysql.connection.cursor()
        dataBase = pymysql.connect(
            host='39.103.183.155',  # MySQL服务端的IP地址
            port=3306,  # MySQL默认PORT地址(端口号)
            user='root',  # 用户名
            password='xx3721xx',  # 密码,也可以简写为passwd
            database='user',  # 库名称,也可以简写为db
            charset='utf8',  # 字符编码
            autocommit=True
        )
        cur = dataBase.cursor()
        cur.execute("insert into User_info(username, password, email, role) "         # insert data into database if email is not registered
                    "values (%s, %s, %s, %s)",
                    (username, password, email, role))
        #mysql.connection.commit()
        cur.connection.commit()
        #return True
        d['message'] = 'register successfully'
        d['password'] = password
        d['email'] = email
        r = json.dumps(d)
        resp = make_response(r)
        resp.status = '200'
        return resp
    else:
        #return False
        d['message'] = 'email already exists'
        r = json.dumps(d)
        resp = make_response(r)
        resp.status = '404'
        return resp


def check_unique(email):                                                # return true if email is in not database, else false
    #cur = mysql.connection.cursor()
    dataBase = pymysql.connect(
        host='39.103.183.155',  # MySQL服务端的IP地址
        port=3306,  # MySQL默认PORT地址(端口号)
        user='root',  # 用户名
        password='xx3721xx',  # 密码,也可以简写为passwd
        database='user',  # 库名称,也可以简写为db
        charset='utf8',  # 字符编码
        autocommit=True
    )
    cur = dataBase.cursor()
    cur.execute("select * from User_info where email=%s", [email])
    if cur.fetchone() is None:
        return True
    else:
        return False


def all_users():
    #cur = mysql.connection.cursor()
    dataBase = pymysql.connect(
        host='39.103.183.155',  # MySQL服务端的IP地址
        port=3306,  # MySQL默认PORT地址(端口号)
        user='root',  # 用户名
        password='xx3721xx',  # 密码,也可以简写为passwd
        database='user',  # 库名称,也可以简写为db
        charset='utf8',  # 字符编码
        autocommit=True
    )
    cur = dataBase.cursor()
    cur.execute("select * from User_info")
    info = cur.fetchall()                       # get all users' data
    for diction in info:
        for k, v in diction.items():
            if v is None:                       # if the value is None, set value to string Null
                diction[k] = 'Null'
    return info                                 # return tuple of user info dicts ({user1 info},{user2 info},{...})


@app.route('/login', methods=['GET', 'POST'])
def get_login_info():
    if request.method == 'POST':
        info = request.json
        d = {
             'message': None,
             'email': info['email'],
             'role': None,
             'cookies': '111',
             'token': 'abc'
             }
        check_user = user_login(info['email'], info['password'])                # two lists to check role and return user's data
        print(check_user)
        # check_admin = admin_login(info['email'], info['password'])              # [True, {'email':'xxx','name':'xxx', ...}] / [False]
        if check_user[0]:                                                       # if login request is user, redirect to user's dashboard
            d['message']='user login successfully'
            d['user_info']= check_user[1]
            d['role']= check_user[1][4]
            r = json.dumps(d)
            resp = make_response(r)
            resp.status = '200'
            return resp
        else:                                                                   # return False status to page if login request cannot be found in database
            d['message'] = 'login failed'
            r = json.dumps(d)
            resp = make_response(r)
            resp.status = '404'
            return resp


@app.route('/dashboard/<login_status>/<user_info>/<email>/<role>', methods=['GET', 'POST'])
def dashboard(login_status, user_info, email, role):
    if request.method == 'POST':
        info=request.json
        if request.json['action'] == 'Modify':                                  # if get modify request
            return redirect(url_for('modify', email=email, role=role))          # redirect to modify page with email and role(admin/user)
        elif request.json['action'] == 'Delete':                                # if get delete request
            return redirect(url_for('delete', email=email, role=role))          # redirect to delete page with email and role(only admin)
    return render_template('dashboard.html', login_status=login_status,
                           user_info=user_info, email=email, role=role)


def get_user_info(email):
    #cur = mysql.connection.cursor()
    dataBase = pymysql.connect(
        host='39.103.183.155',  # MySQL服务端的IP地址
        port=3306,  # MySQL默认PORT地址(端口号)
        user='root',  # 用户名
        password='xx3721xx',  # 密码,也可以简写为passwd
        database='user',  # 库名称,也可以简写为db
        charset='utf8',  # 字符编码
        autocommit=True
    )
    cur = dataBase.cursor()
    cur.execute("select * from User_info where email=%s", (email,))
    info = cur.fetchone()
    return info                                                                 # return a dictionary of user data


def user_login(email, password):
    #cur = mysql.connection.cursor()
    dataBase = pymysql.connect(
        host='39.103.183.155',  # MySQL服务端的IP地址
        port=3306,  # MySQL默认PORT地址(端口号)
        user='root',  # 用户名
        password='xx3721xx',  # 密码,也可以简写为passwd
        database='user',  # 库名称,也可以简写为db
        charset='utf8',  # 字符编码
        autocommit=True
    )
    cur = dataBase.cursor()
    cur.execute("select * from User_info "
                "where email=%s and password=%s",
                (email, password))
    info = cur.fetchone()
    if info is None:                                        # if email and password do not match in User database, return [False]
        return [False]
    else:                                                   # else return True and dictionary of user data
        return True, info


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == "POST":
        delete_email = request.json['email']                                        # Get the email need to be deleted
        #cur = mysql.connection.cursor()
        dataBase = pymysql.connect(
            host='39.103.183.155',  # MySQL服务端的IP地址
            port=3306,  # MySQL默认PORT地址(端口号)
            user='root',  # 用户名
            password='xx3721xx',  # 密码,也可以简写为passwd
            database='user',  # 库名称,也可以简写为db
            charset='utf8',  # 字符编码
            autocommit=True
        )
        cur = dataBase.cursor()
        cur.execute("select * from User_info where email=%s", (delete_email,))      # find this email in User database
        exist = cur.fetchone()
        if exist is None:                                                           # if cannot find email in database
            d = {'message': 'Delete failed, cannot find email',
                 'email': delete_email,
                 'cookies': '111',
                 'token': 'abc'
                 }
            r = json.dumps(d)
            resp = make_response(r)
            resp.status = '404'
            return resp
        else:                                                                       # if find email in database, delete it
            #cur1 = mysql.connection.cursor()
            dataBase = pymysql.connect(
                host='39.103.183.155',  # MySQL服务端的IP地址
                port=3306,  # MySQL默认PORT地址(端口号)
                user='root',  # 用户名
                password='xx3721xx',  # 密码,也可以简写为passwd
                database='user',  # 库名称,也可以简写为db
                charset='utf8',  # 字符编码
                autocommit=True
            )
            cur1 = dataBase.cursor()
            cur1.execute("delete from User_info where email=%s", (delete_email,))
            cur1.connection.commit()
            d = {'message': 'Delete Successfully',
                 'email': delete_email,
                 'cookies': '111',
                 'token': 'abc'
                 }
            r = json.dumps(d)
            resp = make_response(r)
            resp.status = '200'
            return resp


@app.route('/modify', methods=['GET', 'POST'])
def modify():
    if request.method == "POST":
        email = request.json['email']
        modify_info = request.json['modify_info']
        d = {
            "Modified_email": email,
            'cookies': '111',
            'token': 'abc'
        }
        if modify_info['password'] and not password_check(modify_info['password']):                             # return error message to page if password voilates rules
            d["message"] = "Modify failed. Error: Invalid Password"
            r = json.dumps(d)
            resp = make_response(r)
            resp.status = '404'
            return resp
        modify_status = modify_user_info(email, modify_info)
        if not modify_status:
            d["message"] = "Modify failed. Error: Cannot find email"
            r = json.dumps(d)
            resp = make_response(r)
            resp.status = '404'
            return resp
        else:
            d["message"] = "Modify Successfully"
            r = json.dumps(d)
            resp = make_response(r)
            resp.status = '200'
            return resp


def modify_user_info(email, modify_info):
    if check_unique(email):                                                     # return false if cannot find email in database
        return False
    else:                                                                       # else update data
        #cur = mysql.connection.cursor()
        dataBase = pymysql.connect(
            host='39.103.183.155',  # MySQL服务端的IP地址
            port=3306,  # MySQL默认PORT地址(端口号)
            user='root',  # 用户名
            password='xx3721xx',  # 密码,也可以简写为passwd
            database='user',  # 库名称,也可以简写为db
            charset='utf8',  # 字符编码
            autocommit=True
        )
        cur = dataBase.cursor()
        if modify_info['username']:
            cur.execute("update User_info set username=%s where email=%s",
                        (modify_info['username'], email))
        if modify_info['password']:
            cur.execute("update User_info set password=%s where email=%s",
                        (modify_info['password'], email))
        if modify_info['name']:
            cur.execute("update User_info set name=%s where email=%s",
                        (modify_info['name'], email))
        if modify_info['age']:
            cur.execute("update User_info set age=%s where email=%s",
                        (int(modify_info['age']), email))
        cur.connection.commit()
    return True


def password_check(password):
    if len(password)<8 or type(password) != str:    # return false if password length less than 8 or not string
        return False
    for c in password:                              # return false if password contains non-numeric/non-alpha char
        if not c.isalnum():                         # can only contain 0-9, A-Z, a-z
            return False
    return True


def email_check(email):
    if len(email) > 50 or '@' not in email:         # return false if email length exceed 50 or no @ symbol
        return False
    l = email.split('@')                            # e.g. recipient_name @ domain_name . top_level_domain
    if len(l) > 2 or l[1] == '':                    # return false if more than 1 @ or no domain name
        return False
    recipient = l[0]
    domain = l[1].split('.')                        # e.g. domain_name.top_level_domain
    if len(domain) < 2 or '' in domain:             # return false if missing top level domain or domain name
        return False
    return True


if __name__ == '__main__':
    app.run(debug=1)
    cont_sql()

