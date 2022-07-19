# Author: Zixin Li
from flask import Flask, render_template, request, url_for, make_response
from flask_mysqldb import MySQL
from werkzeug.utils import redirect
import json
# from requests import *
import pymysql
from CRUD import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def user_register():
    if request.method == "POST":
        info = request.json
        return add_user(info['username'], info['password'], info['email'], 'User')


@app.route('/admin_add', methods=['GET', 'POST'])
def admin_add():
    if request.method == "POST":
        info = request.json
        return add_user(info['username'], info['password'], info['email'], info['role'])


@app.route('/login', methods=['GET', 'POST'])
def email_login():
    if request.method == 'POST':
        info = request.json
        return login(info['email'], info['password'])


@app.route('/delete', methods=['GET', 'POST'])
def delete_user():
    if request.method == "POST":
        email = request.json['email'] # Get the email need to be deleted
        return delete(email)


@app.route('/user_update', methods=['GET', 'POST'])
def user_update():
    if request.method == "POST":
        email = request.json['email']
        update_info = request.json['update_info']
        print(email, update_info)
        return update(email, update_info)


@app.route('/admin_update', methods=['GET', 'POST'])
def admin_update():
    if request.method == "POST":
        email = request.json['email']
        update_info = request.json['update_info']
        print(email, update_info)
        return update(email, update_info)


if __name__ == '__main__':
    app.run(debug=1)
