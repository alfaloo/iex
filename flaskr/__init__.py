import os
from flask import Flask
from flask_migrate import Migrate
from flaskr import auth, user, patient, diagnosis, main
from .models import db
from dotenv import load_dotenv

# brew services start mysql
# flask --app flaskr run --debug


print("Loading environment variables...")
load_dotenv()

migrate = Migrate()

def create_app(test_config=None):

    print("Creating Flask app...")

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    print("Registering blueprints...")

    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(patient.bp)
    app.register_blueprint(diagnosis.bp)
    app.register_blueprint(main.bp)

    app.add_url_rule('/', endpoint='index')

    print("Flask app created.")

    return app

app = create_app()