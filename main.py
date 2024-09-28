from flask import Flask, render_template, request, redirect, url_for, flash, session 
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
 
with app.app_context(): 
    db.create_all() 
 
@app.route('/register', methods=['GET', 'POST']) 
def register(): 
    if request.method == 'POST': 
        username = request.form.get('username') 
        password = request.form.get('password') 
 
        user = User.query.filter_by(username=username).first() 
        if user: 
            flash('Username already exists', 'error') 
            return redirect(url_for('register')) 
 
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256') 
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
            flash('Oppsies! Account not found, please try again', 'error') 
            return redirect(url_for('login')) 
 
        session['user_id'] = user.id 
        flash('Pop the confetti! You are officially logged in!', 'success') 
        return redirect(url_for('profile')) 
 
    return render_template('login.html') 
 
@app.route('/profile') 
def profile(): 
    user_id = session.get('user_id') 
    if not user_id: 
        flash('Please log in to view your profile', 'error') 
        return redirect(url_for('login')) 
 
    user = User.query.filter_by(id=user_id).first() 
 
    return render_template('profile.html', user=user) 
 
@app.route('/logout') 
def logout(): 
    session.pop('user_id', None) 
    flash('See you later! You have been logged out.', 'success') 
    return redirect(url_for('login')) 
 
@app.route('/reset_password', methods=['GET', 'POST']) 
def reset_password(): 
    user_id = session.get('user_id') 
    if not user_id: 
        flash('Please log in to reset your password', 'error') 
        return redirect(url_for('login')) 
 
    user = User.query.filter_by(id=user_id).first() 
 
    if request.method == 'POST': 
        new_password = request.form.get('new_password') 
        confirm_password = request.form.get('confirm_password') 
 
        if not new_password or not confirm_password: 
            flash('Do not leave us hanging- complete all the details!', 'error') 
            return redirect(url_for('reset_password')) 
 
        if new_password != confirm_password: 
            flash('Oh no! Passwords do not match!', 'error') 
            return redirect(url_for('reset_password')) 
 
        hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256') 
        user.password = hashed_password 
        db.session.commit() 
 
        flash('Password has been reset successfully!', 'success') 
        return redirect(url_for('login')) 
 
    return render_template('resetpw.html', user=user) 
 
@app.route('/delete_account', methods=['POST']) 
def delete_account(): 
    user_id = session.get('user_id') 
    if not user_id: 
        flash('Please log in to delete your account', 'error') 
        return redirect(url_for('login')) 
 
    user = User.query.filter_by(id=user_id).first() 
 
    if user: 
        db.session.delete(user) 
        db.session.commit()
        session.clear() 
 
        flash('Oh oh your account has been deleted. See you again!', 'success') 
        return redirect(url_for('register')) 
 
    flash('User not found.', 'error') 
    return redirect(url_for('profile')) 
 
@app.route('/') 
def home(): 
    return render_template('overview.html') 
 
@app.route('/overview') 
def overview(): 
    return render_template('overview.html') 
 
@app.route('/jheneaiko') 
def jheneaiko(): 
    return render_template('jheneaiko.html') 
 
@app.route('/lana') 
def lana(): 
    return render_template('lana.html') 
 
@app.route('/kaliuchis') 
def kaliuchis(): 
    return render_template('kaliuchis.html') 
 
@app.route('/seating') 
def seating(): 
    return render_template('seating.html') 
 
@app.route('/booking') 
def booking(): 
    return render_template('booking.html') 
 
@app.route('/checkout') 
def checkout(): 
    if 'user_id' not in session:
        flash('Please log in to proceed to checkout', 'error')
        return redirect(url_for('login'))
    
    return render_template('checkout.html') 

@app.route('/about') 
def about(): 
    return render_template('about.html') 
 
if __name__ == "__main__": 
    app.run(debug=True)
