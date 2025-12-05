from flask import Flask, request, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)

# ---- VERİTABANI ----
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# ---- MODELLER ----
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    token = db.Column(db.String(200))
    is_admin = db.Column(db.Boolean, default=False)

class Mesai(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    date = db.Column(db.String(50))
    start = db.Column(db.String(10))
    end = db.Column(db.String(10))
    status = db.Column(db.String(20), default="Bekliyor")

# ---- KULLANICI KAYIT ----
@app.post("/register")
def register():
    data = request.json
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Bu email zaten kayıtlı"}), 400

    new_user = User(
        email=data["email"],
        password=data["password"],
        token=str(uuid.uuid4())
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"success": True})

# ---- GİRİŞ ----
@app.post("/login")
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"], password=data["password"]).first()

    if not user:
        return jsonify({"error": "Hatalı email veya şifre"}), 401

    return jsonify({
        "token": user.token,
        "user_id": user.id,
        "is_admin": user.is_admin
    })

# ---- MESAİ OLUŞTUR ----
@app.post("/mesai/create")
def create_mesai():
    data = request.json
    new_mesai = Mesai(
        user_id=data["user_id"],
        date=data["date"],
        start=data["start"],
        end=data["end"]
    )
    db.session.add(new_mesai)
    db.session.commit()
    return jsonify({"success": True})

# ---- KULLANICI TALEPLERİNİ LİSTELE ----
@app.get("/mesai/list")
def list_mesai():
    user_id = request.args.get("user_id")
    rows = Mesai.query.filter_by(user_id=user_id).all()
    result = [
        {"id": r.id, "date": r.date, "start": r.start, "end": r.end, "status": r.status}
        for r in rows
    ]
    return jsonify(result)

# ---- ADMİN PANELİ ----
@app.get("/admin")
def admin_panel():
    rows = Mesai.query.all()
    html = """
<html>
<head><title>Mesai Yönetimi</title></head>
<body>
<h1>Admin Panel</h1>
</body>
</html>
"""

    <h1>Mesai Talepleri</h1>
    <table border='1' cellpadding='5'>
      <tr><th>ID</th><th>Kullanıcı</th><th>Tarih</th>
