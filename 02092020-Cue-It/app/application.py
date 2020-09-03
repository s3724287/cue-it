# main.py

from flask import request, redirect, url_for, render_template, send_from_directory, Flask
import pandas as pd 
import pandas as pandas
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from csv import reader
import os
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import *
from google.cloud import automl


main = Blueprint('main', __name__)

# CONFIGURATION
ALLOWED_EXTENSIONS = {'xlsx', 'csv'}

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            process_file(os.path.join(UPLOAD_FOLDER, filename), filename, )
            
            
    return render_template('profile.html')
#
def process_file(path, filename):
    prep_cue(path, filename)       
#
def prep_cue(path, filename):
# REPLACING CHARS & CLEAING UP MUSIC CUE SHEET UPLOAD FOR NLP TO ANALYSE
    input_file = pd.DataFrame()
    input_file = pandas.read_excel(path)
    input_file['trackTitle'] = input_file['trackTitle'].str.replace('_', ' ')
    input_file['trackTitle'] = input_file['trackTitle'].str.replace('.WAV', ' ')
    input_file['trackTitle'] = input_file['trackTitle'].str.replace('.new', ' ')
    input_file['trackTitle'] = input_file['trackTitle'].str.replace('.01', ' ')
    input_file['trackTitle'] = input_file['trackTitle'].str.replace('Bounced', ' ')
    for content in range(len(input_file)):            
                predict(input_file['trackTitle'][content])


def predict(content):
    """Predict."""
    # [START automl_language_entity_extraction_predict]

    # TODO(developer): Uncomment and set the following variables
    project_id = "CueIt_1597295266173"
    model_id = "TEN2582705534645829632"

    prediction_client = automl.PredictionServiceClient()

    # Get the full path of the model.
    model_full_id = prediction_client.model_path(
        project_id, "us-central1", model_id
    )

    # Supported mime_types: 'text/plain', 'text/html'
    # https://cloud.google.com/automl/docs/reference/rpc/google.cloud.automl.v1#textsnippet
    text_snippet = automl.types.TextSnippet(
        content=content, mime_type="text/plain"
    )
    payload = automl.types.ExamplePayload(text_snippet=text_snippet)

    response = prediction_client.predict(model_full_id, payload)

    for annotation_payload in response.payload:
        print(
            "Text Extract Entity Types: {}".format(
                annotation_payload.display_name
            )
        )
        print(
            "Text Score: {}".format(annotation_payload.text_extraction.score)
        )
        text_segment = annotation_payload.text_extraction.text_segment
        print("Text Extract Entity Content: {}".format(text_segment.content))
        print("Text Start Offset: {}".format(text_segment.start_offset))
        print("Text End Offset: {}".format(text_segment.end_offset))
    # [END automl_language_entity_extraction_predict]




def allowed_file(filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#@application.route('/uploads/<filename>')
#def uploaded_file():
#    return send_from_directory(application.config['DOWNLOAD_FOLDER'], processed_file, as_attachment=True)