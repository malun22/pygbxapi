import os
from flask import Flask, request
from view_functionalities.analyze import Analyze

app = Flask(__name__)

# Constants
TEMP_UPLOAD_FOLDER = "temp"
MAX_USER_CONTENT_SIZE = 0.25 * 1024 * 1024 * 1024


@app.route("/analyze", methods=["POST"])
def hello_world():
    return Analyze.post(request)


if __name__ == "__main__":

    app.config["TEMP_UPLOAD_FOLDER"] = os.path.join(
        app.root_path, TEMP_UPLOAD_FOLDER)
    app.config["MAX_CONTENT_LENGTH"] = 40 * 1024 * 1024  # 40 MB

    app.run(debug=True)
