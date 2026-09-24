from database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

class Deployment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    bot_name = db.Column(db.String(100), nullable=False)
    plan = db.Column(db.String(50), nullable=False)
    payment = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default="Pending")
