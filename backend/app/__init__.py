from flask import Flask
from flask_cors import CORS
import sys
from pathlib import Path

def create_app():
    app = Flask(__name__)

    # Enable CORS for frontend integration
    CORS(app)

    # Add the backend directory to the path to import route
    backend_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(backend_dir))

    # Register API blueprint
    from route import api
    app.register_blueprint(api, url_prefix='/api')

    return app
