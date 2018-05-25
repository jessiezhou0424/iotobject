from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import  DataRequired
from flask_wtf import FlaskForm

#登录表单
class Login_Form(FlaskForm):
    name=StringField('name',validators=[DataRequired()])
    pwd=PasswordField('pwd',validators=[DataRequired()])
    submit=SubmitField('Login in')


#注册表单
class Register_Form(FlaskForm):
    name=StringField('name',validators=[DataRequired()])
    pwd=PasswordField('pwd',validators=[DataRequired()])
    submit=SubmitField('register')