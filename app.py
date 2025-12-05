from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mesai.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ----------------------------
# MODELLER
# ----------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


class Mesai(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.String(10), nullable=False)
    end_time = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default="pending")  # pending / approved / rejected


with app.app_context():
    db.create_all()


# ----------------------------
# KAYIT OL
# ----------------------------
@app.post("/register")
def register():
    data = request.json
    email = data.get("email")
    password = generate_password_hash(data.get("password"))

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered"})


# ----------------------------
# LOGIN
# ----------------------------
@app.post("/login")
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or

