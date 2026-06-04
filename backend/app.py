from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

from model import db, User, Service

from Management.household_services_api import households_bp

#Caching
import redis
from flask_caching import Cache

# Configurations

app = Flask(__name__)

# Cache configuration
redis_client = redis.Redis(host= 'localhost', port=6379, db=0)
cache = Cache(app, config={'CACHE_TYPE':'redis', 'CACHE_REDIS': redis_client})

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///households.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'household_services'


# Blueprint Registration
app.register_blueprint(households_bp, url_prefix='/api')


# Initializations

db.init_app(app)
CORS(app, origins='*')
jwt = JWTManager(app)
api = Api(app, prefix='/api')


from Management.auth_api import Register, Login, Logout


api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Creating Initial Data

        # Creating Admin 
        if User.query.filter_by(username= 'admin').first() is None:
            admin_password = generate_password_hash('adminadmin')

            admin = User(username='admin', email= 'admin@gmail.com', password=admin_password, role= 'admin', approved = True)

            db.session.add(admin)
            db.session.commit()

        else:
            print("Admin already exists.")

        # Creating Services
        if Service.query.count() == 0:
            Cleaning = Service(name='House Cleaning', description='Clean every corner of your home', price=500, time_required=2)

            db.session.add_all([Cleaning])
            db.session.commit()

        else:
            print("Services already exist.")

    app.run(debug=True)