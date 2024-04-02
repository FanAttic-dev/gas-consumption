
from pathlib import Path
from flask import Flask, abort, Blueprint, url_for, request, send_file
from flask import current_app as app

from werkzeug.utils import secure_filename

from src.constants import DIR_FIGURES, DIR_CSV, MIN_IMAGES
from src.data_analyzer import DataAnalyzer
from src.digit_extractor_morphology import DigitExtractorMorphology


from config import Config


api = Blueprint('api', __name__)


@api.route('/')
def index():
    return 'index'

def validate_file(file) -> bool:
    if len(file.filename) == 0:
        return False
    
    ext = Path(file.filename)
    if ext.suffix not in Config.UPLOAD_EXTENSIONS:
        return False
    
    return True

@api.route('/upload', methods=["POST"])
def upload_images():
    # TODO: solve users
    
    for file in request.files.getlist('file'):
        file.filename = secure_filename(file.filename)
        if validate_file(file):
            file.save(Config.UPLOAD_PATH / file.filename)
        else:
            abort(400)
    return "Files uploaded successfully"
    
    
@api.route('/process_images', methods=["GET"])
def process_images():
    paths = list(Config.UPLOAD_PATH.iterdir())
    if len(paths) < MIN_IMAGES:
        return f"Not enough images uploaded: {len(paths)}/{MIN_IMAGES}", 404
    
    try:
        de = DigitExtractorMorphology(Config.UPLOAD_PATH)
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
        api.logger.exception(e)
        return abort(400)
    

        

