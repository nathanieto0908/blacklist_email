import os
from functools import wraps
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

STATIC_TOKEN = os.environ.get('STATIC_TOKEN', 'token-local-dev')


def simple_token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if auth != f'Bearer {STATIC_TOKEN}':
            return {'message': 'Unauthorized'}, 401
        return fn(*args, **kwargs)
    return wrapper
