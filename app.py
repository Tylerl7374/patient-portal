from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Remember to set this securely
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)

# Define the User model for SQLite
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    clinic_code = db.Column(db.String(20), nullable=False)

# Patient Portal
@app.route('/')
def index():
    return redirect(url_for('login'))

# Register new user
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

    return render_template('registration.html')

# Login route for patients
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = user.username
            return redirect(url_for('patient_dashboard'))
        else:
            return "Invalid login", 400

    return render_template('index.html')

# Patient Dashboard Route
@app.route('/patient-dashboard')
def patient_dashboard():
    if 'username' in session:
        return render_template('patient-dashboard.html')
    return redirect(url_for('login'))

# Provider Portal Route
@app.route('/provider-portal')
def provider_portal():
    return render_template('provider-portal.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    db.create_all()  # Create SQLite tables if not exist
    app.run(debug=True)
