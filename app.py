from flask import Flask, request
from flask_uploads import UploadSet, configure_uploads, ALL

from utils.config_parser import CONVERTER, POST_URL
from settings import CACHE_DIR
from os import path

import requests
import subprocess, shlex

app = Flask(__name__)

# setting up uploader
fbx_files = UploadSet('fbx', ALL)
app.config['UPLOADED_FBX_DEST'] = CACHE_DIR
configure_uploads(app, fbx_files)

@app.route('/converter', methods=['GET', 'POST'])
def converter():

    if request.method == 'POST':
        # saving the file
        fbx_file = request.files['fbx_file']
        fbx_file_name = fbx_files.save(fbx_file)

        # convert file to gltf
        shell_command = f'{CONVERTER} --binary \
            --input {path.join(CACHE_DIR, fbx_file_name)} \
            --output {path.join(CACHE_DIR, fbx_file_name[:-4])}.glb'
        subprocess.run(args=shell_command, shell=True)
        print('file converted')

        # send result back
        files = {'fbx_file': open(f'{path.join(CACHE_DIR, fbx_file_name[:-4])}.glb', 'rb')}
        requests.post(POST_URL, files=files, data={'instructions' : 'for_database'})

        return f"<h1> file recived: {fbx_file_name} </h1>"
    return "<h1> Service is active </h1>"

if __name__ =='__main__':
    app.run(debug=True, port=8081)