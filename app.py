from flask import Flask, request
from flask_uploads import UploadSet, configure_uploads, All
import subprocess

app = Flask(__name__)

fbx_files = UploadSet('fbx', All)
app.config['UPLOAD_FBX_DIST'] = 'fbx_files'
configure_uploads(app, fbx_files)

@app.route('converter')
def converter():
    if request.method is 'POST' and 'thefile' in request.files:
        # convert file to gltf
        subprocess.run(args=["ls ~/"], shell=True)

if __name__ =='__main__':
    app.run(debug=True, host="127.0.0.2")