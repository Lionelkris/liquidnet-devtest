from dotenv import load_dotenv
from flask import Flask
import liquidnet
from liquidnet import config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

load_dotenv()
db = SQLAlchemy()
ma = Marshmallow()


def create_app(configuration=config.DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(configuration)

    db.init_app(app)
    ma.init_app(app)
    from liquidnet.library.routes import library
    from liquidnet.library.models import User, Books, BookRequests
    with app.app_context():

        db.create_all()
        from liquidnet.library import routes
        app.register_blueprint(routes.library)
        from liquidnet.library.library_service import create_book
        create_book()
        return app
