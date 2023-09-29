import os
import shutil
import pandas as pd
from flask_cors import CORS
from flask import Flask, jsonify, request, flash, redirect, Response, make_response
from pathlib import Path
app = Flask(__name__)
CORS(app)
app.config['MONGODB_SETTINGS'] = {
    'db': "health_app",
    'host': "mongodb://127.0.0.1:27017/"
}
app.config['SECRET_KEY'] = "123"


from login import login, signup
from chat import get_all_messages, post_message, upload_file


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
