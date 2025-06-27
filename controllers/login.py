from flask import render_template, request, redirect, url_for, session, Blueprint
from models.file import db, User, Admin

login_bp = Blueprint('login_bp', __name__)

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    userid = request.form.get('User ID')
    password = request.form.get('Password')

    admin = Admin.query.filter_by(admin=userid).first()
    user = User.query.filter_by(userid=userid).first()

    if admin:
        if admin.password == password:
            session.clear()
            session['admin'] = admin.admin
            return redirect(url_for('admin_bp.admin_home'))
        else:
            return render_template('login.html', error="Wrong password. Please try again.")

    elif user:
        if user.password == password:
            session.clear()
            session['user'] = user.userid
            return redirect(url_for('user_bp.user_home', userid=user.userid))
        else:
            return render_template('login.html', error="Wrong password. Please try again.")

    else:
        return render_template('login.html', error="User ID not found. Please register first.")


@login_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    username = request.form['username']
    name = request.form['name']
    email = request.form['email']
    address = request.form['address']
    pincode = request.form['pincode']
    password = request.form['password']
    confirm = request.form['confirm_password']

    if password != confirm:
        return render_template('signup.html', error="Passwords do not match.")

    if User.query.filter_by(userid=username).first():
        return render_template('signup.html', error="User ID already registered.")

    user = User(userid=username, fullname=name, email=email,
                password=password, Address=address, pincode=pincode)
    db.session.add(user)
    db.session.commit()

    return render_template('login.html', error="Account created successfully! Please log in.")


@login_bp.route('/logout')
def logout():
    session.clear()
    return render_template('login.html', error="Logged out successfully.")
