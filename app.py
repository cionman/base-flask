import os
from flask import Flask
from flask import request
from flask import session
from flask import redirect
from flask import render_template
from flask_wtf import CSRFProtect

from models import db
from models import Fcuser
from forms import RegisterForm, LoginForm

app = Flask(__name__)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('userid', None)
    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['userid'] = form.data.get('userid')
        return redirect('/')

    return render_template('login.html', form = form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        fcuser = Fcuser()
        fcuser.userid = form.data.get('userid')
        fcuser.username = form.data.get('username')
        fcuser.password = form.data.get('password')

        db.session.add(fcuser) # 저장

        return redirect('/')

    return render_template('register.html', form = form)

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