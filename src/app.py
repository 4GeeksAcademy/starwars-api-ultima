"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Personaje,Planetas,Vehiculos,Favoritos
from sqlalchemy import select
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)

    # ENDPOINTS


@app.route('/user', methods=['GET'])
def handle_hello():
    all_users = db.session.execute(select(User)).scalars().all()
    result = list(map(lambda item: item.serialize(), all_users))
    if not result:
        return jsonify({"msg": "No users found"}), 404

    response_body = {
        "msg": "ok",
        "result": result
    }

    return jsonify(response_body), 200


@app.route('/user/<int:user_id>', methods=['GET'])
def handle_user(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"msg": "User not found"}), 404

    response_body = {
        "msg": "ok",
        "result": user.serialize()
    }

    return jsonify(response_body), 200


@app.route('/personaje', methods=['GET'])
def handle_personaje():
    all_personajes = db.session.execute(select(Personaje)).scalars().all()
    result = list(map(lambda item: item.serialize(), all_personajes))
    if not result:
        return jsonify({"msg": "No personajes found"}), 404

    response_body = {
        "msg": "ok",
        "result": result
    }

    return jsonify(response_body), 200


@app.route('/personaje/<int:personaje_id>', methods=['GET'])
def handle_personaje_id(personaje_id):
    personaje = db.session.get(Personaje, personaje_id)
    if personaje is None:
        return jsonify({"msg": "personaje not found"}), 404

    response_body = {
        "msg": "ok",
        "result": personaje.serialize()
    }

    return jsonify(response_body), 200

    
@app.route('/planetas', methods=['GET'])
def handle_planetas():
    all_planetas = db.session.execute(select(Planetas)).scalars().all()
    result = list(map(lambda item: item.serialize(), all_planetas))
    if not result:
        return jsonify({"msg": "No planetas found"}), 404

    response_body = {
       "msg": "ok",
       "result": result
       }
    
    return jsonify(response_body), 200
  
@app.route('/planetas/<int:planeta_id>', methods=['GET'])
def handle_planeta_id(planeta_id):
    planeta = db.session.get(Planetas, planeta_id)
    if planeta is None:
        return jsonify({"msg": "planeta not found"}), 404

    response_body = {
        "msg": "ok",
        "result": planeta.serialize()
    }

    return jsonify(response_body), 200

@app.route('/vehiculos', methods=['GET'])
def handle_vehiculos():
    all_vehiculos = db.session.execute(select(Vehiculos)).scalars().all()
    result = list(map(lambda item: item.serialize(), all_vehiculos))
    if not result:
        return jsonify({"msg": "No vehiculos found"}), 404

    response_body = {
       "msg": "ok",
       "result": result
       }
    
    return jsonify(response_body), 200 
 
@app.route('/vehiculos/<int:vehiculo_id>', methods=['GET'])
def handle_vehiculo_id(vehiculo_id):
    vehiculo = db.session.get(Vehiculos, vehiculo_id)
    if vehiculo is None:
        return jsonify({"msg": "vehiculo not found"}), 404

    response_body = {
        "msg": "ok",
        "result": vehiculo.serialize()
    }

    return jsonify(response_body), 200


@app.route('/users/favoritos', methods=['GET'])
def handle_user_favorites():
    user = db.session.get(User, 1)  # Aquí se asume que el ID del usuario es 1, puedes cambiarlo según tus necesidades  
    if user is None:
        return jsonify({"msg": "User not found"}), 404


    response_body = {
       "msg": "ok",
       "result": user.serialize()
       }


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
