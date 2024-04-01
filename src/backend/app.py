from pathlib import Path
from flask import Flask, abort
from flask import url_for, request, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

from services.constants import DIR_FIGURES, DIR_CSV, MIN_IMAGES
from services.data_analyzer import DataAnalyzer
from services.digit_extractor_morphology import DigitExtractorMorphology

app = Flask(__name__, static_url_path='/static')
cors = CORS(app)

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 5 # MAX 5MB
app.config['UPLOAD_EXTENSIONS'] = ['.jpg']
app.config['UPLOAD_PATH'] = Path('static/uploads')
app.config['UPLOAD_PATH'].mkdir(exist_ok=True)


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
    # TODO: solve users
    
    for file in request.files.getlist('file'):
        file.filename = secure_filename(file.filename)
        if validate_file(file):
            file.save(app.config['UPLOAD_PATH'] / file.filename)
        else:
            abort(400)
    return "Files uploaded successfully"
    
    
@app.route('/process_images', methods=["GET"])
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
    app.run("127.0.0.1", 5000)
