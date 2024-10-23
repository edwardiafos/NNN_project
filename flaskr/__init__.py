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
from pathlib import Path


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
    
    THIS_FOLDER = Path(__file__).parent.resolve() # path/to/root/folder/NNN_Project/flaskr

    sys.path.append(f'{THIS_FOLDER}/blueprints.py')
    from blueprints import prediction_bp, upload_bp, catalogue_bp # used to be 'from . import blueprints'
    app.register_blueprint(prediction_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(catalogue_bp)


    return app

app = create_app()

if __name__ == "__main__":
    waitress.serve(app, host='0.0.0.0', port=10000, url_scheme='https')