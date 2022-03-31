from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
supported = app.config["SUPPORTED_LANGUAGES"]
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"
CORS(app)  ## To allow direct AJAX calls


from app import routes, models
