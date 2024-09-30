import flask
import os
from flask import Flask, render_template, request, url_for, redirect, session
from werkzeug.utils import secure_filename
import torch
from torch import nn
import torchvision
import numpy as np
import waitress
import sys


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev"
    )


    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)

    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    app.config["UPLOAD_FOLDER"] = r"upload"


    @app.route('/', methods=["GET", "POST"])
    def index():
        return render_template("index.html")
    

    sys.path.append(r'flaskr\blueprints.py')
    from blueprints import prediction_bp, upload_bp # used to be 'from . import blueprints'
    app.register_blueprint(prediction_bp)
    app.register_blueprint(upload_bp)


    return app

app = create_app()

if __name__ == "__main__":
    waitress.serve(app, host='0.0.0.0', port=10000)