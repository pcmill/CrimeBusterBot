# Serving the model
Based on [keras-flask-deploy-webapp](https://github.com/mtobeiyf/keras-flask-deploy-webapp)

## Installation

### Install requirements

```shell
$ pip install -r requirements.txt
```

Make sure you have the following installed:
- tensorflow
- keras
- flask
- pillow
- h5py
- gevent

### Run with Python

Python 2.7 or 3.5+ are supported and tested.

```shell
$ python app.py
```

------------------

## Customization

### Use your own model

A trained model is placed in the models folder. When you train your own model you need to adjust line 25 of app.py accodingly. If you changed any of the image sizes while you trained (or the way you preprocess the images) you need to apply this in the `resize_with_pad` function that begins on line 32.

### Run the app

```
$ python app.py
```

You should get a link to the localhost where the app is running.

Gunicorn is used in the deployed version on [Heroku](https://webshop-checker-api.herokuapp.com/).

