from flask import Flask
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def ping():
    return str(datetime.utcnow())