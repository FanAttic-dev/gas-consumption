from flask import Flask
from flask import url_for

app = Flask(__name__)


@app.route('/')
def index():
    return 'indexx'


if __name__ == "__main__":
    app.run("127.0.0.0", 5000)
