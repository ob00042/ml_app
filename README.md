ML App
=====

## Requirements
* pip install Flask \
For numpy:
* sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose
* pip install scipy
* pip install sklearn

## To run
From ml_app directory: \
`python app/app.py`

## Details
This app takes a file, saves it in the ml_app/app/uploads directory.
It uses the csv file to create a model, and predict the data.
Then the user can upload another csv file to test,
or enter the data directly in the inputs.