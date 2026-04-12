import uuid

from flask import request
from flask_restful import Resource
from extensions import db, simple_token_required
from models import Blacklist
from schemas import blacklist_schema


def _normalize_app_uuid(value):
    try:
        return str(uuid.UUID(str(value).strip()))
    except (ValueError, AttributeError, TypeError):
        return None


class BlacklistCreate(Resource):
    @simple_token_required
    def post(self):
        data = request.get_json(silent=True) or {}

        email = data.get('email')
        app_uuid = data.get('app_uuid')
        reason = data.get('blocked_reason')

        if not email or not app_uuid:
            return {'message': 'email y app_uuid son obligatorios'}, 400

        app_uuid_norm = _normalize_app_uuid(app_uuid)
        if app_uuid_norm is None:
            return {'message': 'app_uuid debe ser un UUID válido'}, 400

        if reason and len(reason) > 255:
            return {'message': 'blocked_reason no puede superar 255 caracteres'}, 400

        existing = Blacklist.query.filter_by(email=email).first()
        if existing:
            return {'message': 'El email ya se encuentra en la lista negra'}, 400

        ip_address = (
            request.headers.get('X-Forwarded-For', request.remote_addr)
            .split(',')[0]
            .strip()
        )

        entry = Blacklist(
            email=email,
            app_uuid=app_uuid_norm,
            blocked_reason=reason,
            ip_address=ip_address,
        )
        db.session.add(entry)
        db.session.commit()

        return {
            'message': 'Email agregado a lista negra exitosamente',
            'data': blacklist_schema.dump(entry),
        }, 201


class BlacklistCheck(Resource):
    @simple_token_required
    def get(self, email):
        entry = Blacklist.query.filter_by(email=email).first()
        if not entry:
            return {'is_blacklisted': False, 'blocked_reason': None}, 200
        return {'is_blacklisted': True, 'blocked_reason': entry.blocked_reason}, 200
