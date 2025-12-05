from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)

# ---- DATABASE ----
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


# ---- REGISTER ----
@app.post("/register")
def register():
    data = request.json

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Bu email zaten kayıtlı"}), 400

    new_user = User(
        email=data["email"],
        password=data["password"],
        token=str(uuid.uuid4()),
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"success": True})


# ---- LOGIN ----
@app.post("/login")
def login():
    data = request.json

    user = User.query.filter_by(email=data["email"], password=data["password"]).first()
    if not user:
        return jsonify({"error": "Hatalı giriş"}), 401

    return jsonify({
        "token": user.token,
        "user_id": user.id,
        "is_admin": user.is_admin
    })


# ---- MESAİ OLUŞTUR ----
@app.post("/mesai/create")
def create_mesai():
    data = request.json

    row = Mesai(
        user_id=data["user_id"],
        date=data["date"],
        start=data["start"],
        end=data["end"],
    )
    db.session.add(row)
    db.session.commit()

    return jsonify({"success": True})


# ---- MESAİ LİSTELE ----
@app.get("/mesai/list")
def mesai_list():
    user_id = request.args.get("user_id")
    rows = Mesai.query.filter_by(user_id=user_id).all()

    return jsonify([
        {
            "id": r.id,
            "date": r.date,
            "start": r.start,
            "end": r.end,
            "status": r.status
        }
        for r in rows
    ])


# ---- ADMIN API ----
@app.get("/admin/list")
def admin_list():
    rows = Mesai.query.all()

    return jsonify([
        {
            "id": r.id,
            "user_id": r.user_id,
            "date": r.date,
            "start": r.start,
            "end": r.end,
            "status": r.status
        }
        for r in rows
    ])


# ---- BOOT ----
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
    @app.post("/create-admin")
def create_admin():
    email = "admin@example.com"
    password = "Admin123!"
    # Admin oluştur
    cur.execute("INSERT INTO users (email, password, is_admin) VALUES (?, ?, ?)",
                (email, password, 1))
    conn.commit()
    return {"message": "Admin user created", "email": email}

