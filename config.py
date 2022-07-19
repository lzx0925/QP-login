HOST = '39.103.183.155'
PORT = 3306
DATABASE = 'user'
USERNAME = 'root'
PASSWORD = 'xx3721xx'
DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME, password=PASSWORD, host=HOST, port=PORT, db=DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = True

#SQLALCHEMY_DATAbase_URI = 'mysql+pymysql://root:xxxxx@localhost:3306/test?charset=utf8'
#SQLALCHEMY_TRACK_MODIFICATIONS = True