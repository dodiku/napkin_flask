import os
from flask import Flask, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/<group_name>/', methods=['GET', 'POST'])
def group_page(group_name):
    group = Group.get_or_create(group_name)

    if request.method == 'POST':
        json = request.get_json()
        if json:
            group.add_post(getattr(json, 'url', ''), getattr(json, 'text', ''))

    return jsonify(group.serialize())


if __name__ == '__main__':
    app.run()
