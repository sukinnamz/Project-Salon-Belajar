from flask import Flask,render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///salon.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    nama = db.Column(db.String(1000))
    nomor = db.Column(db.String(17))
    status = db.Column(db.String(100))

db.create_all()
    

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/prosesLogin', methods=['POST'])
def proses_login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if (user.password != password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))
    else:
        flash("Failed, check your detail and try again")
    
    session['username'] = user.name
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/pesanan')
def pesanan():
    return render_template('pesanan.html')

@app.route('/insertpesanan')
def insertpesanan():
    return render_template('insertpesan.html')

@app.route('/pengurus')
def pengurus():
    return render_template('pengurus.html')

@app.route('/insertpengurus')
def insertpengurus():
    return render_template('insertpengurus.html')

@app.route('/pengurusProses', methods=['POST'])
def proses_pengurus():
    email = request.form.get('email')
    nama = request.form.get('nama')
    nomor = request.form.get('telepon')
    password = request.form.get('password')
    status= request.form.get('status')

    user = User.query.filter_by(email=email).first() 

    if user: 
        flash('Pengurus telah terdaftar')
        return redirect(url_for('pengurus'))
    
    new_user = User(email=email, nama=nama, password=password, nomor=nomor, status=status)

    
    db.session.add(new_user)
    db.session.commit()

    flash("Sukses ditambahkan")
    return redirect(url_for('pengurus'))

@app.route('/laporan')
def laporan():
    return render_template('laporan.html')


app.run(host='127.0.0.1', port=5000, debug=True)