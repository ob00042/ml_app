from flask import Flask, render_template, request, jsonify, redirect, flash
import os
from werkzeug.utils import secure_filename
# import csv
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
import random
from sklearn import svm

app = Flask(__name__)
app.config['filename_train'] = ''
app.config['model'] = None
app.config['categories'] = None
app.config['columns'] = None


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
    model = request.form.get('model')
    if model == 'rf':
        app.config['model'] = rf
    elif model == 'svm':
        app.config['model'] = svm
    else:
        app.config['model'] = rf

    df = pd.read_csv('app/uploads/' + app.config['filename_train'], delimiter=';', skipinitialspace=True)

    arr, y = process_file(df)

    train_features, test_features, train_labels, test_labels = train_test_split(arr, y, test_size=0.2, random_state=42)

    # Cross Validation Params

    # param_grid = {
    #     'max_depth': [2, 10, 40, 80, None],
    #     'max_features': [2, 3],
    #     'min_samples_leaf': [3, 4, 5],
    #     'min_samples_split': [8, 10, 12],
    #     'n_estimators': [25, 100, 200, 300, 1000]
    # }
    #
    # rf = RandomForestClassifier()
    # # Instantiate the grid search model
    # grid_search = GridSearchCV(estimator=rf, param_grid=param_grid,
    #                            cv=3, n_jobs=-1, verbose=0)
    #
    # grid_search.fit(train_features, train_labels)
    #
    # print(grid_search.best_params_)
    # best_grid = grid_search.best_estimator_
    # grid_accuracy, grid_preds = test_preds(best_grid, test_features, test_labels)
    #
    # print(grid_accuracy)
    # print(grid_preds)
    #
    # app.config['rf_model'] = best_grid
    # acc = grid_accuracy

    acc = train(app.config['model'], train_features, train_labels, test_features, test_labels)

    options = create_options()

    return jsonify({'status': 'Analysed', 'accuracy': acc, 'options': options})


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

    acc, preds = test_preds(app.config['model'], arr, y)

    return jsonify({"status": "tested", "accuracy": acc, "predictions": preds})


@app.route("/direct", methods=['POST', 'OPTIONS'])
def direct():
    data = request.json['data']
    df = pd.DataFrame(data, index=[0])
    arr, y = process_file(df)
    acc, preds = test_preds(app.config['model'], arr, y)

    return jsonify({"status": "tested", "accuracy": acc, "predictions": preds})


def process_file(df):

    if app.config['columns'] is None:
        app.config['columns'] = df.columns

    if app.config['categories'] is None:
        app.config['categories'] = {}
        app.config['categories']['job'] = dict(enumerate(pd.Categorical(df.job).categories))
        app.config['categories']['marital'] = dict(enumerate(pd.Categorical(df.marital).categories))
        app.config['categories']['education'] = dict(enumerate(pd.Categorical(df.education).categories))
        app.config['categories']['default'] = dict(enumerate(pd.Categorical(df.default).categories))
        app.config['categories']['housing'] = dict(enumerate(pd.Categorical(df.housing).categories))
        app.config['categories']['loan'] = dict(enumerate(pd.Categorical(df.loan).categories))
        app.config['categories']['contact'] = dict(enumerate(pd.Categorical(df.contact).categories))
        app.config['categories']['month'] = dict(enumerate(pd.Categorical(df.month).categories))
        app.config['categories']['duration'] = dict(enumerate(pd.Categorical(df.duration).categories))
        app.config['categories']['campaign'] = dict(enumerate(pd.Categorical(df.campaign).categories))
        app.config['categories']['pdays'] = dict(enumerate(pd.Categorical(df.pdays).categories))
        app.config['categories']['previous'] = dict(enumerate(pd.Categorical(df.previous).categories))
        app.config['categories']['poutcome'] = dict(enumerate(pd.Categorical(df.poutcome).categories))
        if 'y' in df:
            app.config['categories']['y'] = dict(enumerate(pd.Categorical(df.y).categories))
        for c in df.columns:
            if c not in app.config['categories']:
                app.config['categories'][c] = None

    if 'y' in df:
        df = df[app.config['columns']]
    else:
        cols = list(app.config['columns'])
        cols.remove('y')
        df = df[cols]

    df['job'] = pd.Categorical(df.job, categories=app.config['categories']['job'].values()).codes
    df['marital'] = pd.Categorical(df.marital, categories=app.config['categories']['marital'].values()).codes
    df['education'] = pd.Categorical(df.education, categories=app.config['categories']['education'].values()).codes
    df['default'] = pd.Categorical(df.default, categories=app.config['categories']['default'].values()).codes
    df['housing'] = pd.Categorical(df.housing, categories=app.config['categories']['housing'].values()).codes
    df['loan'] = pd.Categorical(df.loan, categories=app.config['categories']['loan'].values()).codes
    df['contact'] = pd.Categorical(df.contact, categories=app.config['categories']['contact'].values()).codes
    df['month'] = pd.Categorical(df.month, categories=app.config['categories']['month'].values()).codes
    df['duration'] = pd.Categorical(df.duration, categories=app.config['categories']['duration'].values()).codes
    df['campaign'] = pd.Categorical(df.campaign, categories=app.config['categories']['campaign'].values()).codes
    df['pdays'] = pd.Categorical(df.pdays, categories=app.config['categories']['pdays'].values()).codes
    df['previous'] = pd.Categorical(df.previous, categories=app.config['categories']['previous'].values()).codes
    df['poutcome'] = pd.Categorical(df.poutcome, categories=app.config['categories']['poutcome'].values()).codes
    if 'y' in df:
        df['y'] = pd.Categorical(df.y, categories=app.config['categories']['y'].values()).codes

    arr = df.to_numpy()

    if 'y' in df:
        y = arr[:, -1]
        arr = arr[:, :-1]
    else:
        y = None

    return arr, y


def train(rf, train_features, train_labels, test_features, test_labels):
    rf.fit(train_features, train_labels)

    predictions = rf.predict(test_features)
    c = 0
    for p, ry in zip(predictions, test_labels):
        if p == ry:
            c += 1
    acc = c / len(test_labels)
    return acc


def test_preds(rf, arr, y=None):
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
            preds.append('no')
        else:
            preds.append('yes')
    return acc, preds


def create_options():
    opts = {}
    for k, it in app.config['categories'].items():
        if not it:
            opts[k] = None
        else:
            opts[k] = list(it.values())
    return opts


# run the server
if __name__ == '__main__':
    best = {'max_depth': None, 'max_features': 3, 'min_samples_leaf': 3, 'min_samples_split': 8, 'n_estimators': 300}
    rf = RandomForestClassifier(**best)
    svm = svm.SVC(gamma='scale')
    app.run(debug=True)
