from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import sqlite3
import os
import uuid
import json

con = sqlite3.connect('database.db', check_same_thread=False)
cur = con.cursor()

app = Flask(__name__)

UPLOAD_FOLDER = './profpic/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def page():
    return 'Hello World!'

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/upload_pic', methods=['POST' ,'GET'])
def upload_pic():
    if request.method == 'POST':
        if 'file' not in request.files:
            return '-1'
        file = request.files['file']
        if file.filename == '':
            return '-2'
        if file and allowed_file(file.filename):
            file_ext = file.filename.split(".")[1]
            filename = str(uuid.uuid4()) +"."+ file_ext
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            obj = {"uploadedPic": url_for('download_file', name= filename)}
            return json.dumps(obj)




@app.route('/profile', methods=['POST', 'GET'])
def curr_profile():
    query = cur.execute("SELECT * FROM user ORDER BY id DESC").fetchone()
    obj = {"username": query[1],
           "email": query[2],
           "uploadedPic": query[3],
           "headline": query[4],
           "aboutme": query[5],
           "fullName": query[6]
    }
    return json.dumps(obj)

@app.route('/update_profile', methods=['POST','GET'])
def update_profile():
    if request.method == 'POST':
        if request.json:
            jsonReq = request.json
            jsonLoad = jsonReq
            try:
                query = "INSERT INTO user (username, email, profilepic, headline, aboutme, fullname) VALUES ('{}','{}','{}','{}','{}','{}')".format(jsonLoad['username'], jsonLoad['email'],jsonLoad['uploadedPic'],jsonLoad['headline'],jsonLoad['aboutme'], jsonLoad['fullName'])
                cur.execute(query)
                print(query)

                return redirect(curr_profile)
            except KeyError:
                err = {"error": -1}
                return "-1"


    else:
        return '-1'

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.run()
