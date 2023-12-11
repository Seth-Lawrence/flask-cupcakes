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
    """gets data about all cupcakes.
    Returns JSON {cupcakes: [{id, flavor, size, rating, image_url}, ....]}"""

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)



@app.get('/api/cupcakes/<int:cupcake_id>')
def get_cupcake_data(cupcake_id):
    """get data about a single cupcake
    Return JSON {cupcake: {id, flavor, size, rating, image_url}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.post('/api/cupcakes')
def create_cupcake():
    """Create a cupcake with flavor, size,
    rating and image data from the body of the request.
    Accepts JSON: {flavor, size, rating, image_url}
    Returns JSON: {cupcake: {id, flavor, size, rating, image_url}}
    """

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image_url = request.json["image_url"]

    new_cupcake = Cupcake(
        flavor=flavor,
        size=size,
        rating=rating,
        image_url=image_url
    )
    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)


@app.route('/api/cupcakes/<int:cupcake_id>',methods=['PATCH'])
def update_cupcake(cupcake_id):
    """Updating a cupcake by id
    accept JSON {flavor, size, rating, image_url} but not all field required
    returns newly updated cupcake {cupcake: id, flavor,size,rating,image_url}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    # turn to an object loop -> key:value pairs
    # if request.json['flavor'] true -> assign if not -> current value
    # turn to object?
    # flavor = request.get(flavor, current_value).json()

    data = request.json

    cupcake.size = data.get("size",cupcake.size)
    cupcake.rating = data.get("rating",cupcake.rating)
    cupcake.flavor = data.get("flavor",cupcake.flavor)
    cupcake.image_url = data.get("image_url",cupcake.image_url)

    db.session.add(cupcake)
    db.session.commit()

    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)



@app.route('/api/cupcakes/<int:cupcake_id>',methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Deleting a cupcake by id
    Return JSON {deleted: [cupcake_id]}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify({"deleted": [cupcake_id]})






