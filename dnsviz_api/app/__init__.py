import sys

from flask import Flask, Blueprint
from flask_cors import CORS
from flask_talisman import Talisman
from flask_restful import Api

from dnsviz_api.app.resources.TrustTree import TrustTree

def create_app(app_config:'Config' = None) -> Flask:
    '''Flask application factory
    
    Args:
        app_config: Defaults to None. Contain application config values.

    Returns:
        Configured Flask app

    '''
    app = Flask(__name__)

    # Enable CORS
    CORS(app)

    if app_config is not None:
        app.config.from_object(app_config)

    with app.app_context():
        # Set security headers for production
        if app.config['USE_TALISMAN']:
            Talisman(app)

        api_bp = Blueprint('api_bp', __name__)
        api = Api(api_bp)

        api.add_resource(TrustTree, '/trust-tree', '/trust-tree/<string:hostname>')

        app.register_blueprint(api_bp)

        return app



