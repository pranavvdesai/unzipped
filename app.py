from flask import Flask,render_template,request,redirect,session,flash,redirect,url_for
import os

app= Flask(__name__)
app.secret_key=os.urandom(24)




@app.route('/',methods=['GET', 'POST'])
def index():
     return render_template('home.html')




if __name__ == '__main__':
    app.run(debug=True)
