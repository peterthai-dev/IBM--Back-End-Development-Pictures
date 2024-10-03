from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """Return all pictures"""
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Retrieve a picture by its ID"""
    picture = next((item for item in data if item["id"] == id), None)
    if picture:
        return jsonify(picture), 200
    return {"message": "Picture not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Create a new picture"""
    new_picture = request.get_json()
    if any(item["id"] == new_picture["id"] for item in data):
        return {"Message": f"picture with id {new_picture['id']} already present"}, 302
    data.append(new_picture)
    return jsonify(new_picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Update an existing picture"""
    updated_picture = request.get_json()
    picture = next((item for item in data if item["id"] == id), None)
    if not picture:
        return {"message": "picture not found"}, 404
    picture.update(updated_picture)
    return jsonify(picture), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete a picture by its ID"""
    global data
    picture = next((item for item in data if item["id"] == id), None)
    if not picture:
        return {"message": "picture not found"}, 404
    data = [item for item in data if item["id"] != id]
    return '', 204
