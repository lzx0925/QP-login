from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:xx3721xx@39.103.183.155/user"

db.init_app(app)

print(1)
with app.app_context():
    print(2)
    db.create_all()
    print(13)
    sql_cmd = "select * from user_info"
    query_data = db.engine.execute(sql_cmd).fetchall()
    print(query_data)

if __name__ == "__main__":
    app.run()
