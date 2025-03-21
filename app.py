from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://neondb_owner:npg_onka8geKh9vT@ep-square-scene-a2dczt9x-pooler.eu-central-1.aws.neon.tech/neondb?sslmode=require"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return jsonify({"message": "Neondb working with Flask"})

#Create User
@app.route("/users", methods=["POST"])
def add_user():
    data = request.json
    new_user = Users(name=data["name"], email=data["email"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added", "user":{"id": new_user.id, "email": new_user.email}})

#Get all users
@app.route("/users", methods=["GET"])
def get_users():
    users = Users.query.all()
    return jsonify([{"id": user.id, "name": user.name, "email": user.email} for user in users])

#Update user
@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    user = Users.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    data = request.json
    user.name= data.get("name", user.name)
    user.email= data.get("email", user.email)
    db.session.commit()

    return jsonify({"message": "User updated", "user": {"id": user.id, "name": user.name, "email": user.email}})

#Delete user
@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = Users.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted"})

if __name__=="__main__":
    app.run(debug=True)