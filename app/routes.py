from flask import Flask, render_template
from app import app


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/image1')
def image1():
    return render_template('image1.html')


@app.route('/image2')
def image2():
    return render_template('image2.html')


@app.route('/video1_feed')
def video1_feed():
    return render_template('video1.html')


@app.route('/video2_feed')
def video2_feed():
    return render_template('video2.html')


@app.route('/video1')
def video1():
    return render_template("video1.html")


@app.route('/video2')
def video2():
    return render_template("video2.html")
