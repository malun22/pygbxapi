import os
from website.views import views
from flask import Flask


# Constants
TEMP_UPLOAD_FOLDER = "temp"
MAX_USER_CONTENT_SIZE = 0.25 * 1024 * 1024 * 1024


def create_app():
    app = Flask(__name__)
    app.secret_key = "very secret key"

    app.register_blueprint(views)

    app.config["TEMP_UPLOAD_FOLDER"] = os.path.join(
        app.root_path, TEMP_UPLOAD_FOLDER)
    app.config["MAX_CONTENT_LENGTH"] = 40 * 1024 * 1024  # 40 MB

    return app
