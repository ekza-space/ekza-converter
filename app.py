from flask import Flask, request
from flask_uploads import UploadSet, configure_uploads, ALL

import requests
import subprocess, shlex

app = Flask(__name__)

# setting up uploader
fbx_files = UploadSet('fbx', ALL)
app.config['UPLOADED_FBX_DEST'] = 'static/cloud/fbx_files'
configure_uploads(app, fbx_files)

@app.route('/converter', methods=['GET', 'POST'])
def converter():

    if request.method == 'POST':
        # saving the file
        fbx_file = request.files['fbx_file']
        fbx_file_name = fbx_files.save(fbx_file)

        converter_path = '~/tools/FBX2glTF/FBX2glTF-darwin-x64'

        # convert file to gltf
        shell_command = f'{converter_path} --binary \
            --input ./static/cloud/fbx_files/sphere.fbx \
            --output ./static/cloud/gltf_files/'

        subprocess.run(args=shell_command, shell=True)
        print('file converted')

        return f"<h1> file recived: {fbx_file_name} </h1>"
    return "<h1> page is working </h1>"

if __name__ =='__main__':
    app.run(debug=True, port=8081)