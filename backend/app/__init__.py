from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # Enable CORS for frontend integration
    CORS(app)

    # Register API blueprint
    from ..route import api
    app.register_blueprint(api, url_prefix='/api')

    return app
