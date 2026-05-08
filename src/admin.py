import os
from flask_admin import Admin
from models import db, User, Personaje, Planetas, Vehiculos, Favoritos
from flask_admin.contrib.sqla import ModelView






class FavoritosAdmin(ModelView):
    column_list = ("id", "user", "personaje", "vehiculo", "planeta")


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')
    
    class FavoritosAdmin(ModelView):
        column_list = ("id", "user", "personaje", "vehiculo", "planeta")
        form_columns = ("user", "personaje", "vehiculo", "planeta")

    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Personaje, db.session))
    admin.add_view(ModelView(Planetas, db.session))
    admin.add_view(ModelView(Vehiculos, db.session))

    admin.add_view(FavoritosAdmin(Favoritos, db.session))