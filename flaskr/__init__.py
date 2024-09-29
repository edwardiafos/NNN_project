import flask
import os
from flask import Flask, render_template, request, url_for, redirect, session
from werkzeug.utils import secure_filename
import torch
from torch import nn
import torchvision
import numpy as np


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
    

    from . import blueprints # used to be 'from . import blueprints'
    app.register_blueprint(blueprints.prediction_bp)
    app.register_blueprint(blueprints.upload_bp)


    return app
