from datetime import datetime, timezone
from extensions import db


def _utc_now():
    return datetime.now(timezone.utc)


class Blacklist(db.Model):
    __tablename__ = 'blacklist'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, index=True)
    app_uuid = db.Column(db.String(100), nullable=False)
    blocked_reason = db.Column(db.String(255), nullable=True)
    ip_address = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=_utc_now)
