from models import Fcuser
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms.validators import DataRequired, EqualTo, ValidationError


class RegisterForm(FlaskForm):
    userid = StringField('userid', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('repassword')])
    repassword = PasswordField('re-password', validators=[DataRequired()])


class LoginForm(FlaskForm):
    class CheckPassword(object):

        def __init__(self, message = None) -> None:
            self.message = message

        def __call__(self, form, field):
            userid = form['userid'].data
            password = field.data # password field에 validator로 지정되기때문에 field를 사용할 수 있다.

            fcuser = Fcuser.query.filter_by(userid=userid).first()
            if fcuser.password != password:
                raise ValidationError('패스워드가 맞지 않습니다.')

    userid = StringField('userid', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), CheckPassword()])
