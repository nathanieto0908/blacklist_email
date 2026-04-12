from flask import Flask, jsonify
from flask_restful import Api
from config import Config
from extensions import db, ma, jwt
from resources.blacklist import BlacklistCreate, BlacklistCheck


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    api = Api(app)
    api.add_resource(BlacklistCreate, '/blacklists')
    api.add_resource(BlacklistCheck, '/blacklists/<string:email>')

    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy'}), 200

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=False)
