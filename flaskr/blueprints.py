from flask import Blueprint, request, render_template, session, url_for, redirect, current_app
from werkzeug.utils import secure_filename
import os
import glob
import sys
sys.path.append(r'flaskr\model.py')
from model import get_prediction
from pathlib import Path


prediction_bp = Blueprint(name='prediction', 
               import_name=__name__, 
               url_prefix="/prediction")


@prediction_bp.route('/', methods=("GET", "POST"))
def index():
    return render_template("prediction.html", prediction=session['label'])


upload_bp = Blueprint(name='upload',
                    import_name=__name__,
                    url_prefix="/upload")

@upload_bp.route('/<class_type>', methods=("GET", "POST"))
def index(class_type):
    if request.method == "POST":
            files = glob.glob(f"{current_app.config['UPLOAD_FOLDER']}/*")
            for f in files:
                 os.remove(f) # remove current stored images to free up space

            f = request.files['file']
            filename = secure_filename(f.filename)
            # print(Path(current_app.config['UPLOAD_FOLDER']).is_dir())
            f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            label = get_prediction(model_type=class_type,\
                                   image_path=os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            session.clear()
            session['label'] = label

            return redirect(url_for("prediction.index"))

    page = class_type + ".html"
    return render_template(page, classification_type=class_type)
    