from flask import Flask,render_template,request,redirect,redirect,url_for
import mysql.connector
from app import app

conn=mysql.connector.connect(host="remotemysql.com",user="9YwiYaINDg",password="WB2u9rVHb5",database="9YwiYaINDg")
cursor=conn.cursor()

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin_add',methods=['POST'])
def admin_add():
    global email    
    email=request.form.get('email')
    title=request.form.get('title')
    message=request.form.get('message')
    location=request.form.get('location')
    cursor.execute("""INSERT INTO `admindatabase` (`email`,`title`,`message`,`location`) VALUES ('{}','{}','{}','{}')""".format(email,title,message,location))
    conn.commit()
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    return render_template('userdashboard.html')

@app.route('/dashboard_add',methods=['POST'])
def dashboard_add():
    location=request.form.get('searchlocation')
    cursor.execute("""SELECT * FROM `admindatabase` WHERE `location` LIKE '{}'""".format(location))
    posts=cursor.fetchall()
    print(posts)
    return render_template('userdashboard.html',posts=posts)
