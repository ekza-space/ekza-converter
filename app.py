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

        # convert file to gltf
        converter_path = '~/tools/FBX2glTF/FBX2glTF-darwin-x64'
        shell_command = f'{converter_path} --binary \
            --input ./static/cloud/fbx_files/{fbx_file_name} \
            --output ./static/cloud/gltf_files/{fbx_file_name[:-4]}.glb'
        subprocess.run(args=shell_command, shell=True)
        print('file converted')

        # send result back
        url = 'http://127.0.0.1:8080/converter'
        files = {'fbx_file': open(f'static/cloud/gltf_files/{fbx_file_name[:-4]}.glb', 'rb')}
        requests.post(url, files=files, data={'instructions' : 'for_database'})

        return f"<h1> file recived: {fbx_file_name} </h1>"
    return "<h1> page is working </h1>"

if __name__ =='__main__':
    app.run(debug=True, port=8081)