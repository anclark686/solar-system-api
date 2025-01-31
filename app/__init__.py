from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)

    # DB config
    if not test_config:
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
                "RENDER_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
                "SQLALCHEMY_TEST_DATABASE_URI")
    
    # Import models here
    from app.models.planet import Planet
    from app.models.moon import Moon

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here  
    from .routes.planet_routes import planets_bp
    app.register_blueprint(planets_bp)

    from .routes.moon_routes import moons_bp
    app.register_blueprint(moons_bp)
    
    return app
