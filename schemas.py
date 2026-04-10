from extensions import ma
from models import Blacklist

class BlacklistSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Blacklist

    id = ma.auto_field()
    email = ma.auto_field()
    app_uuid = ma.auto_field()
    blocked_reason = ma.auto_field()
    ip_address = ma.auto_field()
    created_at = ma.auto_field()

blacklist_schema = BlacklistSchema()