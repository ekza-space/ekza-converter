from flask import Flask, request
from flask_uploads import UploadSet, configure_uploads, All
# import requests
import subprocess

app = Flask(__name__)

fbx_files = UploadSet('fbx', All)
app.config['UPLOADED_FBX_DEST'] = 'fbx_files'
configure_uploads(app, fbx_files)

@app.route('/converter')
def converter():

    if request.method is 'POST' and 'thefile' in request.files:
        # convert file to gltf
        print('file recived')
        subprocess.run(args=["ls ~/"], shell=True)

    return "<h1> page is working </h1>"

if __name__ =='__main__':
    app.run(debug=True, host="localhost", port=8081)