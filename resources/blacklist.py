from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from models import Blacklist
from extensions import db
from schemas import blacklist_schema
from extensions import simple_token_required

# POST /blacklists
class BlacklistCreate(Resource):

    @simple_token_required
    def post(self):
        data = request.get_json()

        email = data.get('email')
        app_uuid = data.get('app_uuid')
        reason = data.get('blocked_reason')

        # Validaciones
        if not email or not app_uuid:
            return {"message": "email y app_uuid son obligatorios"}, 400

        if reason and len(reason) > 255:
            return {"message": "blocked_reason máximo 255 caracteres"}, 400

        # Verificar si ya existe
        if Blacklist.query.filter_by(email=email).first():
            return {"message": "El email ya está en lista negra"}, 400

        # Obtener IP
        ip_address = request.remote_addr

        new_entry = Blacklist(
            email=email,
            app_uuid=app_uuid,
            blocked_reason=reason,
            ip_address=ip_address
        )

        db.session.add(new_entry)
        db.session.commit()

        return {
            "message": "Email agregado a lista negra",
            "data": blacklist_schema.dump(new_entry)
        }, 201


# GET /blacklists/<email>
class BlacklistCheck(Resource):

    @simple_token_required
    def get(self, email):
        try:
            entry = Blacklist.query.filter_by(email=email).first()
            if entry:
                return {
                    "blocked": True,
                    "blocked_reason": entry.blocked_reason or "Sin motivo especificado"
                }, 200
            else:
                return {
                    "blocked": False,
                    "blocked_reason": None
                }, 200
        except Exception as e:
            return {"message": str(e)}, 500
    