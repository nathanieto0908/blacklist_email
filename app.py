
from flask import Flask
from flask_restful import Api
from config import Config
from extensions import db, ma, jwt

from resources.blacklist import BlacklistCreate, BlacklistCheck
from flask import request
from functools import wraps

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
ma.init_app(app)
jwt.init_app(app)

api = Api(app)

# Endpoints obligatorios
api.add_resource(BlacklistCreate, '/blacklists')
api.add_resource(BlacklistCheck, '/blacklists/<string:email>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)