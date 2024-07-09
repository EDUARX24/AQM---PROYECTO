from flask import Flask, session, render_template, url_for, request, redirect, flash, jsonify, send_file, flash
import os
from flask_session import Session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import NoSuchColumnError
from sqlalchemy.engine.row import Row
from loginRequired import login_required


app = Flask(__name__)

# VERIFICAR VAR DE ENTORNO
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

os.environ.get("DATABASE_URL")

print(os.environ.get("DATABASE_URL"))
engine = create_engine(os.getenv("DATABASE_URL"))

db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("index.html")

#Ruta registro
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        email = request.form.get("email")
        gender = request.form.get("gender")
        phone = request.form.get("phone")
        password = request.form.get("password")
        print(firstName,lastName,email,gender,phone,password)
        #Verificar campos vacios
        if not firstName or not lastName or not email or not gender or not phone or not password:
            data = {
                'icon': 'error',
                'title': 'Error',
                'text': 'Falto llenar algun campo',
                'redirect': 'register'
            }
            return render_template("notification.html", data=data)
        #Guardar datos 
        query = text('''
            INSERT INTO users (first_name, last_name, email, gender, phone, password_hash, rol) VALUES 
            (:first_name, :last_name, :email, :gender, :phone, :password_hash, :rol)
            ''')
        newUser = db.execute(query, {"first_name": firstName, "last_name": lastName, "email": email, "gender": gender, 
                "phone": int(phone), "password_hash": generate_password_hash(password), "rol": "admin"})
        print(newUser)
        db.commit()
        #Guardar id USUARIO en session
        session["id"] = query
        data = {
            'icon': 'success',
            'title': 'Usuario Registrado',
            'text': 'Te has registrado correctamente',
            'redirect': 'register'
        }
        return render_template("notification.html", data=data)

    return render_template("AUTH/register.html")