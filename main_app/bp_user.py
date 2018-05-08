from  flask import render_template,Blueprint,redirect,url_for,flash
from flask_login import login_user, logout_user,login_required

from main_app.forms.userform import Login_Form,Register_Form
from main_app.models.user import User
from main_app import db
import json

bp = Blueprint('bp_user', __name__)

@bp.route('/')
def index():
    form=Login_Form()
    return render_template('login.html',form=form)

@bp.route('/index')
def l_index():
    form = Login_Form()
    return render_template('login.html',form=form)

@bp.route('/login',methods=['POST'])
def login():
        form=Login_Form()
        if form.validate_on_submit():
            user=User.query.filter_by(name=form.name.data).first()
            if user is not  None and user.pwd==form.pwd.data:
                login_user(user)
                flash('success')
                return  render_template('ok.html',name=form.name.data)
            else:
                flash('wrong username or password')
                return render_template('login.html',form=form)
        return json.dumps({'Response': 'Hello'})

#用户登出
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('loged out')
    return redirect(url_for('bp_user.index'))


@bp.route('/register',methods=['GET','POST'])
def register():
    form=Register_Form()
    if form.validate_on_submit():
        user=User(name=form.name.data,pwd=form.pwd.data)
        db.session.add(user)
        db.session.commit()
        flash('sign up success')
        return redirect(url_for('bp_user.index'))
    return render_template('register.html',form=form)