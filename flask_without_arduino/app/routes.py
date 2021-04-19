from flask import render_template, flash, redirect, url_for, request, json
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
from flask import jsonify

from flask_sqlalchemy import SQLAlchemy
from app.tabl import log

mode = 0
control_mode = ''
flag = False

@app.route('/')
@app.route('/index1', methods = ['POST','GET'])
@login_required
def index1():
    global mode
    global control_mode
    global flag
    result = ''

    if request.method == 'POST':
        if request.form['floor']=='Автоматический режим':
            flag = True #авто режим
        elif request.form['floor'] == '1':
            print('кнопа 1')
            mode = 1
            flag = False
        elif request.form['floor'] == '2':
            print('кнопа 2')
            mode = 2
            flag = False
        elif request.form['floor'] == 'Стоп':
            print('кнопа стоп')
            mode = 0
            flag = False
        print(mode)


    return render_template('index1.html',title='Home', result = result)

@app.route('/update_log', methods=['GET', 'POST'])
def update_log():
    result = log()
    str_log = ''
    for ii in result:
        str_log = str_log + str(ii[0])+"\t"+str(ii[1])+"\t"+str(ii[2])+"\t"+str(ii[3])+"<br />"
    return json.dumps({'result': str_log})


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index1'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index1')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index1'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index1'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/data', methods=['GET'])
def get_data():
    global mode
    global flag

    if flag==False:
        if mode == 0:
            return '0'
        elif mode == 1:
            return '1'
        elif mode == 2:
            return '2'
    else:
        return 'A'
