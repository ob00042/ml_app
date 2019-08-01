from flask import Flask, render_template, request, jsonify, redirect, flash
import os
from werkzeug.utils import secure_filename
import csv
import numpy as np
import pandas as pd

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def hello():
    return render_template('index.html')


@app.route("/upload", methods=["POST"])
def upload():
    if 'csv' not in request.files:
        flash('No file part')
        return redirect(request.url)
    csv = request.files.get('csv')
    filename = secure_filename(csv.filename)
    f = open('app/uploads/' + filename, 'wb+')
    f.close()
    csv.save(os.path.join('app/uploads', filename))
    return jsonify({'status': 'Uploaded'})


@app.route("/analyse", methods=["POST"])
def analyse():
    csv = pd.read_csv('app/uploads/bank-full.csv')
    print(csv.columns)
    print(csv.values[1])
    return jsonify({'status': 'Analysed'})


# run the server
if __name__ == '__main__':
    app.run(debug=True)
