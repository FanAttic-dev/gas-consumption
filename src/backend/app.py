from datetime import timedelta
from pathlib import Path
import shutil
from flask import Flask, abort, jsonify
from flask import url_for, request, send_file
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, unset_jwt_cookies, JWTManager, get_current_user
from werkzeug.utils import secure_filename

from services.database import db
from services.models import User
from services.constants import FIGURES_DIRNAME, CSV_DIRNAME, FILES_FOLDER, MIN_IMAGES, TOKEN_EXPIRATION_DELTA_MINS, UPLOADS_DIRNAME
from services.data_analyzer import DataAnalyzer
from services.digit_extractor_morphology import DigitExtractorMorphology

app = Flask(__name__, static_url_path='/static')
cors = CORS(app)

app.config['JWT_SECRET_KEY'] = "d1542bd969ae4edabfdf34e750c624a5"

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 5 # MAX 5MB
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.JPG']

jwt = JWTManager(app)
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()
    
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


def get_current_user_folder() -> Path:
    user = get_current_user()
    user_folder = FILES_FOLDER / str(user.id)
    user_folder.mkdir(parents=True, exist_ok=True)
    return user_folder

def get_current_user_uploads_folder() -> Path:
    user_folder = get_current_user_folder()
    uploads_folder = user_folder / UPLOADS_DIRNAME
    uploads_folder.mkdir(parents=True, exist_ok=True)
    return uploads_folder

@app.route('/')
@jwt_required()
def index():
    return 'index'

def validate_file(file) -> bool:
    if len(file.filename) == 0:
        return False
    
    ext = Path(file.filename)
    if ext.suffix not in app.config["UPLOAD_EXTENSIONS"]:
        return False
    
    return True

@app.route('/register', methods=["POST"])
def register():
    json = request.get_json()
    name = json["name"]
    password = json["password"]
    
    user = User.query.filter_by(name=name).first()
    if user is not None:
        return jsonify({'success': False, 'message': "User already exists. Please, log in."}), 400
        
    user = User(name, password)
    db.session.add(user)
    db.session.commit()
    
    access_token = create_access_token(identity=user.id)
    
    response = jsonify({'success': True, 'token': access_token})    
    return response, 201

@app.route('/login', methods=["POST"])
def login():
    json = request.get_json()
    
    user = User.authenticate(**json)
    if not user:
        return jsonify({'success': False, 'message': "User does not exist. Please, register."}), 400
        
    access_token = create_access_token(identity=user.id, expires_delta=timedelta(minutes=TOKEN_EXPIRATION_DELTA_MINS))
    
    response = jsonify({'success': True, 'token': access_token})
    return response, 200
   
@app.route('/uploads/<image_name>', methods=["GET"])
@jwt_required()
def get_image(image_name: str):
    try:
        user = get_current_user()
        uploads_folder = FILES_FOLDER / str(user.id) / UPLOADS_DIRNAME
        return str(uploads_folder / image_name)
    except Exception as e:
        return str(e), 400
    
@app.route('/uploads', methods=["GET"])
@jwt_required()
def get_all_images():
    try:
        uploads_folder = get_current_user_uploads_folder()
        
        images = list(map(lambda image: image.name, uploads_folder.iterdir()))
        return jsonify(images)
    except Exception as e:
        return str(e), 400
   
@app.route('/upload', methods=["POST"])
@jwt_required()
def upload_images():
    try:
        uploads_folder = get_current_user_uploads_folder()
        
        for file in request.files.getlist('file'):
            file.filename = secure_filename(file.filename)
            if validate_file(file):
                file.save(str(uploads_folder / file.filename))
            else:
                raise "File validation failed"
            
        return "Files uploaded successfully", 200
    except Exception as e:
        return str(e), 400
    
@app.route('/clear_images', methods=["GET"])
@jwt_required()
def clear_images():
    uploads_folder = get_current_user_uploads_folder()
    shutil.rmtree(uploads_folder)
    return "Images cleared"
    
@app.route('/process_images', methods=["GET"])
@jwt_required()
def process_images():
    user_folder = get_current_user_folder()
    csv_folder = user_folder / CSV_DIRNAME
    figures_folder = user_folder / FIGURES_DIRNAME
    uploads_folder = user_folder / UPLOADS_DIRNAME
    paths = list(uploads_folder.iterdir())
    
    if len(paths) < MIN_IMAGES:
        return f"Not enough images uploaded: {len(paths)}/{MIN_IMAGES}", 404
    
    try:
        de = DigitExtractorMorphology(uploads_folder, csv_folder)
        app.logger.info("Digit Extractor created, processing dataset...")
        de.process_dataset()
        app.logger.info("Dataset processed")
        da = DataAnalyzer(csv_folder, figures_folder)
        app.logger.info("Data Analyzer created, analyzing...")
        da.analyze(show=False)
        app.logger.info("Data Analyzer finised")
        
        chart_file = next(figures_folder.iterdir())
        assert chart_file.exists()
        
        return str(chart_file)
    except Exception as e:
        app.logger.exception(e)
        return abort(400)
    
        
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=3000, debug=True)
