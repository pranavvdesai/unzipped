from flask import Flask, render_template, request, redirect, session, flash, redirect, url_for
from passlib.hash import sha256_crypt
from werkzeug.utils import secure_filename
from app import app
from app import conn
from app import cursor


@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/')


@app.route("/loginvalidation", methods=['POST'])
def loginval():
    global email
    global password
    global displayname
    error = ""
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        cursor.execute(
            """SELECT * FROM `userfashion` WHERE `email` LIKE '{}'""".format(email))
        userfashion = cursor.fetchone()[3]
        if len(userfashion) > 0:
            if sha256_crypt.verify(password, userfashion):
                cursor.execute(
                    """SELECT * FROM `userfashion`  WHERE `email` LIKE '{}'""".format(email))
                user = cursor.fetchone()
                displayname = user[1]
                session['user_id'] = True
                flash('account logged in')
                return redirect(url_for('home'))
            else:
                error = "Wrong Email or Password"
                return render_template('login.html', error=error)
    except Exception as e:
        error = "invalid email. Pls register"
        return render_template('login.html', error=error)


@app.route('/add_user', methods=['POST'])
def add_user():
    global name
    global phone_number
    global gender
    name = request.form.get('username')
    email = request.form.get('useremail')
    password = sha256_crypt.encrypt((str(request.form.get('userpassword'))))
    phone_number = request.form.get('userphone')
    gender = request.form.get('gender')
    cursor.execute("""INSERT INTO `userfashion` (`user_id`,`name`,`email`,`password`,`phone_number`,`gender`) VALUES (NULL,'{}','{}','{}','{}','{}')""".format(
        name, email, password, phone_number, gender))
    conn.commit()
    flash('accoount created')
    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')
