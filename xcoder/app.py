from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Worker

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///freelancing.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Change this to a random secret key

db.init_app(app)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    workers = Worker.query.all()
    return render_template('index.html', workers=workers)

@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('user_register.html')

@app.route('/worker/register', methods=['GET', 'POST'])
def worker_register():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        skills = request.form['skills']
        price = request.form['price']
        new_worker = Worker(username=username, name=name, address=address,
                            phone=phone, skills=skills, price=price)
        db.session.add(new_worker)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('worker_register.html')

@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('user_login.html')

@app.route('/worker/login', methods=['GET', 'POST'])
def worker_login():
    if request.method == 'POST':
        username = request.form['username']
        worker = Worker.query.filter_by(username=username).first()
        if worker:
            session['username'] = username
            return redirect(url_for('profile', username=username))
    return render_template('worker_login.html')

@app.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first()
    worker = Worker.query.filter_by(username=username).first()
    return render_template('profile.html', user=user, worker=worker)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
