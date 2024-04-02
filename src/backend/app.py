from pathlib import Path
from flask import Flask, abort, jsonify
from flask import url_for, request, send_file
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, unset_jwt_cookies, JWTManager
from werkzeug.utils import secure_filename

from services.database import db
from services.models import User
from services.constants import DIR_FIGURES, DIR_CSV, MIN_IMAGES
from services.data_analyzer import DataAnalyzer
from services.digit_extractor_morphology import DigitExtractorMorphology

app = Flask(__name__, static_url_path='/static')
cors = CORS(app)

app.config['JWT_SECRET_KEY'] = "d1542bd969ae4edabfdf34e750c624a5"

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 5 # MAX 5MB
app.config['UPLOAD_EXTENSIONS'] = ['.jpg']
app.config['UPLOAD_PATH'] = Path('static/uploads')
app.config['UPLOAD_PATH'].mkdir(exist_ok=True, parents=True)

jwt = JWTManager(app)
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

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
        
    access_token = create_access_token(identity=user.id)
    
    response = jsonify({'success': True, 'token': access_token})
    return response, 200
   
@app.route('/upload', methods=["POST"])
@jwt_required()
def upload_images():
    # TODO: solve users
    
    for file in request.files.getlist('file'):
        file.filename = secure_filename(file.filename)
        if validate_file(file):
            file.save(app.config['UPLOAD_PATH'] / file.filename)
        else:
            abort(400)
    return "Files uploaded successfully"
    
    
@app.route('/process_images', methods=["GET"])
@jwt_required()
def process_images():
    paths = list(app.config['UPLOAD_PATH'].iterdir())
    if len(paths) < MIN_IMAGES:
        return f"Not enough images uploaded: {len(paths)}/{MIN_IMAGES}", 404
    
    try:
        de = DigitExtractorMorphology(app.config['UPLOAD_PATH'])
        app.logger.info("Digit Extractor created, processing dataset...")
        de.process_dataset()
        app.logger.info("Dataset processed")
        da = DataAnalyzer()
        app.logger.info("Data Analyzer created, analyzing...")
        da.analyze(show=False)
        app.logger.info("Data Analyzer finised")
        
        chart_file = next(DIR_FIGURES.iterdir())
        assert chart_file.exists()
        
        return str(chart_file)
    except Exception as e:
        app.logger.exception(e)
        return abort(400)
    
    
        
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=3000, debug=True)
