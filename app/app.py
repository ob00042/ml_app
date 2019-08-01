from flask import Flask, render_template, request, jsonify, redirect, flash
import os
from werkzeug.utils import secure_filename
# import csv
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)
app.config['filename_train'] = ''

@app.route("/", methods=["GET", "POST"])
def hello():
    return render_template('index.html')


@app.route("/upload", methods=["POST"])
def upload():
    if 'csv' not in request.files:
        flash('No file part')
        return redirect(request.url)
    csv = request.files.get('csv')
    filename_train = secure_filename(csv.filename)
    app.config['filename_train'] = filename_train
    f = open('app/uploads/' + filename_train, 'wb+')
    f.close()
    csv.save(os.path.join('app/uploads', filename_train))
    return jsonify({'status': 'Uploaded'})


@app.route("/analyse", methods=["POST"])
def analyse():
    df = pd.read_csv('app/uploads/' + app.config['filename_train'], delimiter=';', skipinitialspace=True)

    arr, y = process_file(df)

    train_features, test_features, train_labels, test_labels = train_test_split(arr, y, test_size=0.2, random_state=42)

    rf.fit(train_features, train_labels)

    predictions = rf.predict(test_features)
    c = 0
    for p, ry in zip(predictions, test_labels):
        if p == ry:
            c += 1
    acc = c/len(test_labels)

    return jsonify({'status': 'Analysed', 'accuracy': acc})


@app.route('/test', methods=['POST'])
def test():
    if 'test' not in request.files:
        flash('No file part')
        return redirect(request.url)
    test = request.files.get('test')
    filename = secure_filename(test.filename)
    f = open('app/uploads/' + filename, 'wb+')
    f.close()
    test.save(os.path.join('app/uploads', filename))

    df = pd.read_csv(os.path.join('app/uploads', filename), delimiter=';', skipinitialspace=True)

    arr, y = process_file(df)

    predictions = rf.predict(arr)
    if y is not None:
        c = 0
        for p, ry in zip(predictions, y):
            if p == ry:
                c += 1
        acc = c / len(y)
    else:
        acc = None

    preds = []
    for p in predictions:
        if p == 0:
            preds.append('yes')
        else:
            preds.append('no')

    return jsonify({"status": "tested", "accuracy": acc, "predictions": preds})


def process_file(df):
    # df['job'] = df.job.astype('category')
    # df['marital'] = df.marital.astype('category')
    # df['education'] = df.education.astype('category')
    # df['default'] = df.default.astype('category')
    # df['housing'] = df.housing.astype('category')
    # df['loan'] = df.loan.astype('category')
    # df['contact'] = df.contact.astype('category')
    # df['duration'] = df.duration.astype('category')
    # df['campaign'] = df.campaign.astype('category')
    # df['pdays'] = df.pdays.astype('category')
    # df['previous'] = df.previous.astype('category')
    # df['poutcome'] = df.poutcome.astype('category')

    df['job'] = pd.Categorical(df.job).codes
    df['marital'] = pd.Categorical(df.marital).codes
    df['education'] = pd.Categorical(df.education).codes
    df['default'] = pd.Categorical(df.default).codes
    df['housing'] = pd.Categorical(df.housing).codes
    df['loan'] = pd.Categorical(df.loan).codes
    df['contact'] = pd.Categorical(df.contact).codes
    df['month'] = pd.Categorical(df.month).codes
    df['duration'] = pd.Categorical(df.duration).codes
    df['campaign'] = pd.Categorical(df.campaign).codes
    df['pdays'] = pd.Categorical(df.pdays).codes
    df['previous'] = pd.Categorical(df.previous).codes
    df['poutcome'] = pd.Categorical(df.poutcome).codes
    if 'y' in df:
        df['y'] = pd.Categorical(df.y).codes

    arr = df.to_numpy()

    if 'y' in df:
        y = arr[:, -1]
        arr = arr[:, :-1]
    else:
        y = None

    return arr, y


# run the server
if __name__ == '__main__':
    rf = RandomForestClassifier(n_estimators=1000, random_state=42)
    app.run(debug=True)
