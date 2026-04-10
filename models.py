from extensions import db
from datetime import datetime

class Blacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    email = db.Column(db.String(120), nullable=False)
    app_uuid = db.Column(db.String(100), nullable=False)
    
    blocked_reason = db.Column(db.String(255))
    
    ip_address = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Blacklist {self.email}>"