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

def create_blacklist(email, app_uuid, blocked_reason, repo, ip_address=None):
    if not email or not app_uuid:
        raise ValueError("email y app_uuid son obligatorios")

    app_uuid_norm = _normalize_app_uuid(app_uuid)
    if app_uuid_norm is None:
        raise ValueError("UUID inválido")

    if blocked_reason and len(blocked_reason) > 255:
        raise ValueError("blocked_reason muy largo")

    if repo.exists(email):
        raise ValueError("Email ya existe")

    repo.save(email, app_uuid_norm, blocked_reason, ip_address)

    return {
        "message": "Email agregado a lista negra exitosamente"
    }


def get_blacklist(email, repo):
    record = repo.get(email)

    if not record:
        return False, None

    return True, record.blocked_reason

class BlacklistRepo:
    def exists(self, email):
        return Blacklist.query.filter_by(email=email).first() is not None

    def save(self, email, app_uuid, reason, ip):
        entry = Blacklist(
            email=email,
            app_uuid=app_uuid,
            blocked_reason=reason,
            ip_address=ip,
        )
        db.session.add(entry)
        db.session.commit()

    def get(self, email):
        return Blacklist.query.filter_by(email=email).first()



class BlacklistCreate(Resource):
    @simple_token_required
    def post(self):
        data = request.get_json(silent=True) or {}

        email = data.get('email')
        app_uuid = data.get('app_uuid')
        reason = data.get('blocked_reason')

        ip_address = (
            request.headers.get('X-Forwarded-For', request.remote_addr)
            .split(',')[0]
            .strip()
        )

        repo = BlacklistRepo()

        try:
            create_blacklist(email, app_uuid, reason, repo, ip_address)
        except ValueError as e:
            return {"message": str(e)}, 400

        entry = repo.get(email)

        return {
            'message': 'Email agregado a lista negra exitosamente',
            'data': blacklist_schema.dump(entry),
        }, 201
class BlacklistCheck(Resource):
    @simple_token_required
    def get(self, email):
        repo = BlacklistRepo()

        is_blacklisted, reason = get_blacklist(email, repo)

        return {
            'is_blacklisted': is_blacklisted,
            'blocked_reason': reason
        }, 200
