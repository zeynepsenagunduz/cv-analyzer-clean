#app.py
from flask import Flask, json, request, jsonify
import os
import hashlib
import urllib.request
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import PyPDF2 
import time
import string
from helper import *

app = Flask(__name__)
CORS(app, resources={r"/": {"origins": "*"}})

app.secret_key = "caircocoders-ednalan"
 
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['CORS_HEADERS'] = 'Content-Type'
 
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
@app.route('/')
@cross_origin()
def main():
    return 'Homepage'
 

@app.route('/upload', methods=['POST'])
@cross_origin()
def upload_file():

    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        resp.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
        resp.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        resp.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        resp.headers.add('Access-Control-Allow-Credentials', 'true')
        return resp
 
    files = request.files.getlist('files[]')
     
    errors = {}
    success = False
     
    for file in files:      
        if file and allowed_file(file.filename):
            filename = hashlib.sha256(secure_filename(request.form["username"] + str(time.time()).replace('.','')).encode('utf-8')).hexdigest() + '.' + file.filename.rsplit('.', 1)[1].lower()
            #filename = request.form["username"]+ '.' + file.filename.rsplit('.', 1)[1].lower()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = True
        else:
            errors[file.filename] = 'File type is not allowed'
 
    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
    if success:
        resp = jsonify({'message' : 'Files successfully uploaded','filename':filename})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp


@app.route('/process-cv', methods=['POST'])
@cross_origin()
def processCV():

    # get filename from request and extract all text from pdf
    data = request.get_json()
    filename = data['filename']

    #allTextList = handleCV(filename)[0]
    allTextList = handleCV(filename)

    # with open('./outputCV.txt', 'w') as f:
    #     #write line by line
    #     for line in allTextList[0]:
    #         f.write(line + '\n')

    resp = jsonify({'message': 'CV successfully processed','textList': allTextList})
    resp.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
    resp.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    resp.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    resp.headers.add('Access-Control-Allow-Credentials', 'true')
    return resp


@app.route('/jobpost', methods=['POST'])
@cross_origin()
def processJobTextRoute():

    # get filename from request and extract all text from pdf
    data = request.get_json()
    jobText = data['jobtext']

    mylist = processJobText(jobText)
    print('mylist', mylist)
 
    resp = jsonify({'message': 'CV successfully processed','textList': list(set(mylist)) })
    resp.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
    resp.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    resp.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    resp.headers.add('Access-Control-Allow-Credentials', 'true')
    return resp

 
if __name__ == '__main__':
    app.run(debug=True)