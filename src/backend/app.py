from pathlib import Path
from flask import Flask, abort
from flask import url_for, request, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
cors = CORS(app)

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 5 # MAX 5MB
app.config['UPLOAD_EXTENSIONS'] = ['.jpg']
app.config['UPLOAD_PATH'] = 'uploads'



@app.route('/')
def index():
    return 'index'

def validate_file(file) -> bool:
    if len(file.filename) == 0:
        return False
    
    ext = Path(file.filename)
    if ext.suffix not in app.config["UPLOAD_EXTENSIONS"]:
        return False
    
    return True

@app.route('/upload', methods=["POST"])
def upload_images():
    uploads_path = Path(app.config['UPLOAD_PATH'])
    uploads_path.mkdir(exist_ok=True)
    
    # TODO: solve users
    
    for file in request.files.getlist('file'):
        file.filename = secure_filename(file.filename)
        if validate_file(file):
            file.save(uploads_path / file.filename)
        else:
            abort(400)
    return "Files uploaded successfully"
    
@app.route('/uploads/<filename>', methods=["GET"])
def get_image(filename: str):
    path = Path(app.config['UPLOAD_PATH']) / filename
    return send_file(str(path), mimetype='image/jpg')
    
    
        
if __name__ == "__main__":
    app.run("127.0.0.1", 5000)
