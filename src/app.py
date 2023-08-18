"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_all_family_members():
    members = jackson_family.get_all_members()
    if len(members) < 1: return "No members", 200
    response_body = {
        "hello": "Hi we are the Jacksons",
        "family": members
    }

    return jsonify(response_body), 200


@app.route('/add', methods=['POST'])
def add_family_member():
    data = request.json
    if data["name"] == None or data["city"] == None:
        return "Missing parameters for family member", 200
    jackson_family.add_member(data)
    return jsonify(data), 200

    # return jsonify(response_body), 200


@app.route('/members/<int:id>', methods=['GET'])
def get_family_member(id):
    if (id) == 0:
        return "Member id not specified", 400

    member = jackson_family.get_member(id)
    response_body = {
        "family_member": member
    }

    return jsonify(response_body), 200


@app.route('/remove/<int:id>', methods=['DELETE'])
def delete_family_member(id):
    jackson_family.delete_member(id)
    response_body = {
        "message": "The member was removed",
    }

    return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
