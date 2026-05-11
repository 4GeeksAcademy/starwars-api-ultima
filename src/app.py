"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Personaje, Planetas, Vehiculos, Favoritos
from sqlalchemy import select
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token,get_jwt_identity, jwt_required, JWTManager

app = Flask(__name__)
app.url_map.strict_slashes = False
bcrypt = Bcrypt(app)

# DB CONFIG
db_url = os.getenv("DATABASE_URL")
if db_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# INIT
Migrate(app, db)
db.init_app(app)
CORS(app, resources={r"/*": {"origins": "*"}})
setup_admin(app)

# JWT
app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)

# ERROR HANDLER
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# SITEMAP
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# LOGIN


# USERS
@app.route('/user', methods=['GET'])
def get_users():
    users = db.session.execute(select(User)).scalars().all()
    result = [u.serialize() for u in users]

    if not result:
        return jsonify({"msg": "No users found"}), 404

    return jsonify({"msg": "ok", "result": result}), 200


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.session.get(User, user_id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify({"msg": "ok", "result": user.serialize()}), 200


# PERSONAJES
@app.route('/personaje', methods=['GET'])
def get_personajes():
    personajes = db.session.execute(select(Personaje)).scalars().all()
    result = [p.serialize() for p in personajes]

    if not result:
        return jsonify({"msg": "No personajes found"}), 404

    return jsonify({"msg": "ok", "result": result}), 200


@app.route('/personaje/<int:personaje_id>', methods=['GET'])
def get_personaje(personaje_id):
    personaje = db.session.get(Personaje, personaje_id)

    if not personaje:
        return jsonify({"msg": "personaje not found"}), 404

    return jsonify({"msg": "ok", "result": personaje.serialize()}), 200


# PLANETAS
@app.route('/planetas', methods=['GET'])
def get_planetas():
    planetas = db.session.execute(select(Planetas)).scalars().all()
    result = [p.serialize() for p in planetas]

    if not result:
        return jsonify({"msg": "No planetas found"}), 404

    return jsonify({"msg": "ok", "result": result}), 200


@app.route('/planetas/<int:planeta_id>', methods=['GET'])
def get_planeta(planeta_id):
    planeta = db.session.get(Planetas, planeta_id)

    if not planeta:
        return jsonify({"msg": "planeta not found"}), 404

    return jsonify({"msg": "ok", "result": planeta.serialize()}), 200


# VEHICULOS
@app.route('/vehiculos', methods=['GET'])
def get_vehiculos():
    vehiculos = db.session.execute(select(Vehiculos)).scalars().all()
    result = [v.serialize() for v in vehiculos]

    if not result:
        return jsonify({"msg": "No vehiculos found"}), 404

    return jsonify({"msg": "ok", "result": result}), 200


@app.route('/vehiculos/<int:vehiculo_id>', methods=['GET'])
def get_vehiculo(vehiculo_id):
    vehiculo = db.session.get(Vehiculos, vehiculo_id)

    if not vehiculo:
        return jsonify({"msg": "vehiculo not found"}), 404

    return jsonify({"msg": "ok", "result": vehiculo.serialize()}), 200


# FAVORITOS
@app.route('/users/<int:user_id>/favoritos', methods=['GET'])
def get_user_favoritos(user_id):
    user = db.session.get(User, user_id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    favoritos = [f.serialize() for f in user.favoritos]

    return jsonify({"msg": "ok", "result": favoritos}), 200



# DELETE FAVORITE
@app.route('/favorite/<int:favorito_id>', methods=['DELETE'])
def delete_favorite(favorito_id):
    favorito = db.session.get(Favoritos, favorito_id)

    if not favorito:
        return jsonify({"msg": "Favorito not found"}), 404

    db.session.delete(favorito)
    db.session.commit()

    return jsonify({"msg": "Favorito eliminado"}), 200

# signup

@app.route('/signup', methods=['POST'])

def signup():
    body = request.get_json()

    nombre = body.get("nombre")
    apellido = body.get("apellido")
    email = body.get("email")
    password = body.get("password")

    if not nombre or not apellido or not email or not password:
        return jsonify({"msg": "se requieren nombre, apellido, email y contraseña"}), 400
    
    existing_user = db.session.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()

    if existing_user:
        return jsonify({"msg": "Usuario ya existe"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(
        nombre=nombre,
        apellido=apellido,
        email=email,
        password=hashed_password
    )   

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "usuario creado"}), 201

# login
@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    if not email or not password:
        return jsonify({"msg": "se requieren email y contraseña"}), 400

    user = db.session.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()

    if user is None:
        return jsonify({"msg": "email o contraseña incorrectos"}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"msg": "email o contraseña incorrectos"}), 401

    access_token = create_access_token(identity=email)

    return jsonify({
        "msg": "login exitoso",
        "access_token": access_token
    }), 200
# PROTECTED
@app.route("/private", methods=["GET"])
@jwt_required()
def private():
    current_user = get_jwt_identity()
    return jsonify(msg="Acceso autorizado", user=current_user), 200



# RUN SERVER
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

