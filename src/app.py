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
    return jsonify(response_body), 200

#METODOS PARA CREAR USUARIOS, PERSONAJES, PLANETAS Y VEHICULOS
@app.route('/user', methods=['POST'])
def user_post():
    body = request.json
    #busqueda del email del usuario en la base de datos para evitar duplicados
    email=db.session.execute(select(User).where(User.email == body["email"])).scalar_one_or_none()
    if  email  is None:
# si el email no existe, se crea un nuevo objeto User con los datos proporcionados en el cuerpo de la solicitud y se guarda en la base de datos
        usuario_nuevo = User(nombre=body["nombre"], apellido=body["apellido"], email=body["email"], password=body["password"])
        db.session.add(usuario_nuevo)
        db.session.commit()

        response_body = {       
            "msg": "usuario creado",
                                         
            }
        return jsonify(response_body), 201
    
    return jsonify({"msg": "User already exists"}), 400



@app.route('/personaje', methods=['POST'])
def personaje_post():
    body = request.json
#busqueda del nombre del personaje en la base de datos para evitar duplicados
    nombre_personaje=db.session.execute(select(Personaje).where(Personaje.nombre_personaje == body["nombre_personaje"])).scalar_one_or_none()
    if  nombre_personaje  is None:
# si el personaje no existe, se crea un nuevo objeto Personaje con los datos proporcionados en el cuerpo de la solicitud y se guarda en la base de datos
        personaje_nuevo = Personaje(nombre_personaje=body["nombre_personaje"], edad=body["edad"], genero=body["genero"])
        db.session.add(personaje_nuevo)
        db.session.commit()

        response_body = {       
            "msg": "personaje creado",
                                         
            }
        return jsonify(response_body), 201

    return jsonify({"msg": "Personaje already exists"}), 400
    
@app.route('/planetas', methods=['POST'])
def planetas_post():
    body = request.json
#busqueda del nombre del planeta en la base de datos para evitar duplicados
    nombre_planetas=db.session.execute(select(Planetas).where(Planetas.nombre_planetas == body["nombre_planetas"])).scalar_one_or_none()
    if  nombre_planetas  is None:
        # si el planeta no existe, se crea un nuevo objeto Planetas con los datos proporcionados en el cuerpo de la solicitud y se guarda en la base de datos
        planeta_nuevo = Planetas(nombre_planetas=body["nombre_planetas"], habitantes=body["habitantes"], ubicacion=body["ubicacion"])
        db.session.add(planeta_nuevo)
        db.session.commit()

        response_body = {       
            "msg": "planeta creado",
                                         
            }
        return jsonify(response_body), 201
# si el planeta ya existe, se devuelve un mensaje de error indicando que el planeta ya existe
    return jsonify({"msg": "Planeta already exists"}), 400
    
@app.route('/vehiculos', methods=['POST'])
def vehiculos_post():
    body = request.json
#busqueda del nombre del vehiculo en la base de datos para evitar duplicados
    nombre_vehiculos=db.session.execute(select(Vehiculos).where(Vehiculos.nombre_vehiculos == body["nombre_vehiculos"])).scalar_one_or_none()
    if  nombre_vehiculos  is None:
 # si el vehiculo no existe, se crea un nuevo objeto Vehiculos con los datos proporcionados en el cuerpo de la solicitud y se guarda en la base de datos
        vehiculo_nuevo = Vehiculos(nombre_vehiculos=body["nombre_vehiculos"] , modelo=body["modelo"], pasajeros=body["pasajeros"])
        db.session.add(vehiculo_nuevo)
        db.session.commit()

        response_body = {       
            "msg": "vehiculo creado",
                                         
            }
        return jsonify(response_body), 201

    return jsonify({"msg": "Vehiculo already exists"}), 400

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
