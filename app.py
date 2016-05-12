import os
from flask import Flask, request, jsonify, redirect
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *


@app.route('/', defaults={'group_name': None})
@app.route('/<group_name>/', methods=['GET', 'POST'])
def group_page(group_name):
    # Make sure that a group name was given, otherwise generate a name.
    if not group_name:
        return redirect('/{}/'.format(Group.generate_name()))

    # Get or create a group with this name.
    group = Group.get_or_create(group_name)

    # If it's a POST request, create a new post in the group.
    if request.method == 'POST':
        json = request.get_json()
        if json:
            group.add_post(getattr(json, 'url', ''), getattr(json, 'text', ''))

    # Serialize and return the group and its posts.
    return jsonify(group.serialize())


if __name__ == '__main__':
    app.run()
