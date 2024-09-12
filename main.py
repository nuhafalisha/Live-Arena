from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
 
app = Flask(__name__) 

app.config['SECRET_KEY'] = 'your_secret_key_here'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
 
@app.route('/register', methods=['GET', 'POST']) 
def register(): 
    if request.method == 'POST': 
        username = request.form.get('username') 
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists', 'error')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))  
    
    return render_template('register.html') 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash('Invalid credentials, please try again', 'error')
            return redirect(url_for('login'))

        flash('Login successful!', 'success')
        return redirect(url_for('dashboard'))  

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return "Welcome to your dashboard!"
 
 
if __name__ == "__main__": 
    app.run(debug=True)