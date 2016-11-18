from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, redirect, url_for


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jens:@localhost/flask'
app.debug = True
db = SQLAlchemy(app)


class User2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
def index():
    myUser = User2.query.all()
    oneItem = User2.query.filter_by(username='jens').first()
    return render_template('add_user.html', myUser=myUser, oneItem=oneItem)


@app.route('/post_user', methods=['POST'])
def post_user():
    user = User2(request.form['username'], request.form['email'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/profile/<the_username>')
def profile(the_username):
    user = User2.query.filter_by(username=the_username).first()
    return render_template('profile.html', user=user)


if __name__ == '__main__':
    app.run()
