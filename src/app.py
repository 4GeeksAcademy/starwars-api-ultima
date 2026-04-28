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

#endpoint para obtener la lista de favoritos de un usuario específico, incluyendo los detalles de cada favorito 
@app.route('/users/<int:user_id>/favoritos', methods=['GET'])
def handle_user_favoritos(user_id):
    # busqueda del usuario en la base de datos para verificar que existe
    user = db.session.get(User, user_id)

    if user is None:
        return jsonify({"msg": "User not found"}), 404
# si el usuario existe, se obtiene la lista de favoritos del usuario y se serializa cada favorito para incluir los detalles del personaje, vehiculo o planeta asociado
    favoritos = list(map(lambda favorito: favorito.serialize(), user.favoritos))

    response_body = {
        "msg": "ok",
        "result": favoritos

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
#endpoint para agregar un planeta a favoritos
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    # busqueda del planeta en la base de datos para verificar que existe

    existing = db.session.execute(select(Favoritos).where(Favoritos.user_id == 1,Favoritos.id_planetas == planet_id)).scalar_one_or_none()

    if existing:
        return jsonify({"msg": "already exists"}), 400
# si el planeta no existe, se crea un nuevo objeto Favoritos con los datos proporcionados en el cuerpo de la solicitud y se guarda en la base de datos
    new_favorite = Favoritos(user_id=1, id_planetas=planet_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"msg": "Planeta agregado a favoritos"}), 201

#endpoint para agregar un vehiculo a favoritos
@app.route('/favorite/vehiculo/<int:vehiculo_id>', methods=['POST'])
def add_favorite_vehiculo(vehiculo_id):
# busqueda del vehiculo en la base de datos para verificar que existe
    existing = db.session.execute(select(Favoritos).where(Favoritos.user_id == 1,Favoritos.id_vehiculos == vehiculo_id)).scalar_one_or_none()

    if existing:
        return jsonify({"msg": "already exists"}), 400
# si el vehiculo no existe, se crea un nuevo objeto Favoritos con los datos proporcionados en el cuerpo de la solicitud y se guarda en la base de datos
    new_favorite = Favoritos(user_id=1, id_vehiculos=vehiculo_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"msg": "Vehiculo agregado a favoritos"}), 201


#endpoint para agregar un personaje a favoritos
@app.route('/favorite/personaje/<int:personaje_id>', methods=['POST'])
def add_favorite_personaje(personaje_id):

    existing = db.session.execute(select(Favoritos).where(Favoritos.user_id == 1,Favoritos.id_personajes == personaje_id)).scalar_one_or_none()

    if existing:
        return jsonify({"msg": "already exists"}), 400

    new_favorite = Favoritos(user_id=1, id_personajes=personaje_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"msg": "Personaje agregado a favoritos"}), 201
# endpoint para eliminar un favorito de personaje, planeta o vehiculo
@app.route('/favorite/<int:favorito_id>', methods=['DELETE'])
def delete_favorite(favorito_id):
    favorito = db.session.get(Favoritos, favorito_id)

    if favorito is None:
        return jsonify({"msg": "Favorito not found"}), 404

    db.session.delete(favorito)
    db.session.commit()

    return jsonify({"msg": "Favorito eliminado"}), 200


if __name__ == '__main__':
        PORT = int(os.environ.get('PORT', 3000))
        app.run(host='0.0.0.0', port=PORT, debug=False)
