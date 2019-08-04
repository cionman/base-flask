import os

from flask import Flask
from flask import render_template
from flask import session
from flask_wtf import CSRFProtect
from flask_jwt import JWT
from example.api_v1 import api
from example.web import web

from models import db, Fcuser

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/example/api/v1')
app.register_blueprint(web, url_prefix='/example/web')


@app.route('/')
def hello():
    userid = session.get('userid', None)
    return render_template('hello.html', userid=userid)


basedir = os.path.abspath(os.path.dirname(__file__))

# mac에서 mysql 연결 문제 해결 : http://hacks.claztec.net/2018/01/29/flask-flask-sqlalchemy-mysql-setting.html
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost:3306/flask?charset=utf8'  ## 데이터베이스 url mysql8버전 패스워드 보안때문에 mysql+pymysql을 붙여주어야한다.
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  ## 메소드 종료시점에 commit
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ADASsdasd!@#SD23sdwe'  # CSRF 키
app.config['JSON_AS_ASCII'] = False  # API 한글 깨짐 방지

# csrf설정
csrf = CSRFProtect()
csrf.init_app(app)

# db 생성
db.init_app(app)
db.app = app
db.create_all()


# jwt 설정

def authenticate(username, password):
    user = Fcuser.query.filter(Fcuser.userid == username).first()
    if user.password == password:
        return user


def identity(payload):
    userid = payload['identity']
    return Fcuser.query.filter(Fcuser.id == userid).first()


jwt = JWT(app, authenticate, identity)

if __name__ == "__main__":  # 파이썬 명령어로 구동을 위함
    app.run(host='127.0.0.1', port=5000, debug=True)
