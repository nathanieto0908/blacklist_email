from extensions import ma
from models import Blacklist


class BlacklistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Blacklist
        load_instance = True


blacklist_schema = BlacklistSchema()
