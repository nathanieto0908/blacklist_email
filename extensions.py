from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask import request
from functools import wraps

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

STATIC_TOKEN = "3MesesPaSobrevivir"

def simple_token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", None)

        if auth != f"Bearer {STATIC_TOKEN}":
            return {"message": "Unauthorized"}, 401

        return fn(*args, **kwargs)
    return wrapper