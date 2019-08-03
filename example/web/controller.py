from forms import LoginForm, RegisterForm
from models import Fcuser, db
from . import web
from flask import session, redirect, render_template


@web.route('/logout', methods=['GET'])
def logout():
    session.pop('userid', None)
    return redirect('/')


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['userid'] = form.data.get('userid')
        return redirect('/')

    return render_template('login.html', form=form)


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        fcuser = Fcuser()
        fcuser.userid = form.data.get('userid')
        fcuser.username = form.data.get('username')
        fcuser.password = form.data.get('password')

        db.session.add(fcuser)  # 저장

        return redirect('/')

    return render_template('register.html', form=form)
