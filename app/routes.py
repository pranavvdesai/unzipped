from app import app


@app.route('/',methods=['GET', 'POST'])
def index():
     return render_template('home.html')



@app.route('/register')
def register():
    return render_template('register.html')



@app.route('/login')
def login():
    return render_template('login.html')