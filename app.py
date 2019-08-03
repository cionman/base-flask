import os

from flask import Flask
from flask import render_template
from flask import session
from flask_wtf import CSRFProtect
from example.api_v1 import api
from example.web import web

from models import db

app = Flask(__name__)
app.register_blueprint(api, url_prefix = '/example/api/v1')
app.register_blueprint(web, url_prefix = '/example/web')

@app.route('/')
def hello():
    userid = session.get('userid', None)
    return render_template('hello.html', userid = userid)


basedir = os.path.abspath(os.path.dirname(__file__))

# mac에서 mysql 연결 문제 해결 : http://hacks.claztec.net/2018/01/29/flask-flask-sqlalchemy-mysql-setting.html
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost:3306/flask?charset=utf8' ## 데이터베이스 url mysql8버전 패스워드 보안때문에 mysql+pymysql을 붙여주어야한다.
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  ## 메소드 종료시점에 commit
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ADASsdasd!@#SD23sdwe' # CSRF 키

#csrf설정
csrf = CSRFProtect()
csrf.init_app(app)

db.init_app(app)
db.app = app
db.create_all()

if __name__ == "__main__": # 파이썬 명령어로 구동을 위함
    app.run(host='127.0.0.1', port=5000, debug=True)