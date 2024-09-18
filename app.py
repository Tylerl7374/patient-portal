from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Set this securely in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # For development

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    clinic_code = db.Column(db.String(20), nullable=False)

@app.route('/')
def index():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        clinic_code = request.form['clinic_code']

        valid_clinic_codes = ['ABC123', 'XYZ789']  # Clinic-provided codes
        if clinic_code not in valid_clinic_codes:
            return "Invalid clinic code!", 400

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists!", 400

        new_user = User(username=username, password=password, clinic_code=clinic_code)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username, password=password).first()

    if user:
        session['username'] = user.username
        return redirect(url_for('dashboard'))
    else:
        return "Invalid login", 400

if __name__ == '__main__':
    app.run(debug=True)
