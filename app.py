import os

from flask import Flask, request, jsonify
from models import db, connect_db, Cupcake


app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///cupcakes")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

connect_db(app)

"""Flask app for Cupcakes"""


@app.get('/api/cupcakes')
def get_all_cupcake_data():
    """gets data about all cupcakes"""
    ...



@app.get('/api/cupcakes/<int:cupcake-id>')
def get_cupcake_data():
    """get data about a single cupcake"""
    ...


@app.post('/api/cupcakes')
def create_cupcake():
    """Create a cupcake with flavor, size,
    rating and image data from the body of the request."""

    ...


