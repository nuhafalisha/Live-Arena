from flask import Flask, render_template, request, redirect, url_for 
 
app = Flask(__name__) 
 
@app.route('/register', methods=['GET', 'POST']) 
def register(): 
    if request.method == 'POST': 
        username = request.form.get('username') 
        password = request.form.get('password') 
        return redirect(url_for('register')) 
    return render_template('register.html') 
 
 
if __name__ == "__main__": 
    app.run(debug=True)