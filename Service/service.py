#------------------ EXERCISE -------------------#
# --------- Author: Magdalena Kolarova  -------- #

import os
import hashlib
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

app=Flask(__name__)

app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


ALLOWED_EXTENSIONS = set(['jpg', 'txt', 'pdf' ])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file
        if 'file' not in request.files:
            flash('No file')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected!')
            return redirect(request.url)
        # Calculate the contents of the file and convert to MD5
        if file and allowed_file(file.filename):
            md5_hash = hashlib.md5(file.read()).hexdigest()
            return render_template("upload.html", calculated_hash = md5_hash)
        else:
            flash('Allowed file types are jpg, txt, pdf')
            return redirect(request.url)

if __name__ == "__main__":
    app.run(host = '127.0.0.1',port = 4123, debug = False)
