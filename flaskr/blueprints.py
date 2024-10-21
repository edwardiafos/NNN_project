from flask import Blueprint, request, render_template, session, url_for, redirect, current_app, jsonify
from werkzeug.utils import secure_filename
import os
import glob
import sys
from pathlib import Path

THIS_FOLDER = Path(__file__).parent.resolve() # path/to/root/folder/NNN_Project/flaskr

sys.path.append(f'{THIS_FOLDER}/model.py')
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
    preset_image_names = []
    for image_name in os.listdir(THIS_FOLDER / "static" / class_type):
         preset_image_names.append(image_name)

    if request.method == "POST":
            if request.content_type == "application/json":
                image_path = THIS_FOLDER / "static" / class_type / request.get_json()['filename']
                label = get_prediction(model_type=class_type, image_path=image_path)

                session.clear()
                session['label'] = label

                return jsonify(redirect_url=url_for("prediction.index"))

            else:
                files = glob.glob(f"{current_app.config['UPLOAD_FOLDER']}/*")
                for f in files:
                    os.remove(f) # remove current stored images to free up space

                f = request.files['file']
                filename = secure_filename(f.filename)
                f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

                label = get_prediction(model_type=class_type,\
                                    image_path=os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

                session.clear()
                session['label'] = label

                return redirect(url_for("prediction.index"))

    page = class_type + ".html"
    return render_template(page, classification_type=class_type, preset_image_names=preset_image_names)


catalogue_bp = Blueprint(name='catalogue', 
                         import_name=__name__,
                         url_prefix='/catalogue')

@catalogue_bp.route('/<type>', methods=('GET', ))
def index(type):
     webpage = f"{type}_catalogue.html"
     return render_template(webpage)