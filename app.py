from flask import Flask,render_template,request,redirect,session,flash,redirect,url_for
from passlib.hash import sha256_crypt
import mysql.connector
import os
import requests
import cv2
from flask import Response
import urllib.request
from werkzeug.utils import secure_filename
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

app= Flask(__name__)
app.secret_key=os.urandom(24)
 
conn=mysql.connector.connect(host="remotemysql.com",user="9YwiYaINDg",password="######",database="9YwiYaINDg")
cursor=conn.cursor()



@app.route('/',methods=['GET', 'POST'])
def index():
     return render_template('home.html')



@app.route('/register')
def register():
    return render_template('register.html')



@app.route('/login')
def login():
    return render_template('login.html')

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
    error=""
    try:
        email=request.form.get('email')
        password=request.form.get('password')
        cursor.execute("""SELECT * FROM `userfashion` WHERE `email` LIKE '{}'""".format(email))
        userfashion=cursor.fetchone()[3]
        if len(userfashion)>0:
            if sha256_crypt.verify(password,userfashion):
                cursor.execute("""SELECT * FROM `userfashion`  WHERE `email` LIKE '{}'""".format(email))
                user=cursor.fetchone()
                displayname=user[1]
                session['user_id']=True
                flash('account logged in')
                return redirect(url_for('home'))
                # return render_template('home.html',displayname=displayname)
            else:
                error="Wrong Email or Password"
                return render_template('login.html',error=error)
        # else:
        #     errors="invlaid user. pls register"
        #     return render_template('login.html',errors=errors)
            
    except Exception as e:
        error="invalid email.register"
        return render_template('login.html',error=error)


    



    


@app.route('/add_user',methods=['POST'])
def add_user():
    global name    
    global phone_number
    global gender
    name=request.form.get('username')
    email=request.form.get('useremail')
    password=sha256_crypt.encrypt((str(request.form.get('userpassword'))))
    phone_number=request.form.get('userphone')
    gender=request.form.get('gender')
   
    cursor.execute("""INSERT INTO `userfashion` (`user_id`,`name`,`email`,`password`,`phone_number`,`gender`) VALUES (NULL,'{}','{}','{}','{}','{}')""".format(name,email,password,phone_number,gender))
    conn.commit()
    flash('accoount created')
    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')



@app.route('/home', methods=['POST'])
def form_data():
    global result
    if request.method=="POST":
        req=request.form
        movie=req['movie']
        music=req['music']
        sport=req['sport']
        choice=req['choice']
        result=movie+music+sport+choice
        cursor.execute("""SELECT * FROM `userfashion`  WHERE `email` LIKE '{}' AND `password` LIKE '{}' """.format(email,password))
        user=cursor.fetchone()
        cursor.execute("""UPDATE `userfashion` set results='{}' WHERE email='{}' """.format(result,email))
        conn.commit()
        conn.commit()
        return render_template('home.html')







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




UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/image1', methods=['POST'])
def upload_image1():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        np.set_printoptions(suppress=True)
        model = tensorflow.keras.models.load_model('keras_model.h5')
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        image = Image.open(r'/static/uploads/post2.jpeg')
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        image_array = np.asarray(image)
        #image.show()
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        data[0] = normalized_image_array
        prediction = model.predict(data)
        #print(prediction)
        return render_template('image1.html', filename=filename, prediction=prediction)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)



@app.route('/image2', methods=['POST'])
def upload_image2():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        np.set_printoptions(suppress=True)
        model = tensorflow.keras.models.load_model('keras_model.h5')
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        image = Image.open(r'/static/uploads/post1.jpeg')
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        image_array = np.asarray(image)
        #image.show()
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        data[0] = normalized_image_array
        prediction = model.predict(data)
        #print(prediction)
        return render_template('image1.html', filename=filename, prediction=prediction)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

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










if __name__ == '__main__':
    app.run(debug=True)


# error handler

# @app.errorhandler(404)
# def error_handler_page(e):
#     return render_template('error.html')
