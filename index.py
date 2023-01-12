from flask import Flask, request, jsonify
import json

app = Flask(__name__)

countries = [
    {"id":"1","name":"Thailand","capital":"Bangkok"},
    {"id":"2","name":"Australia","capital":"Canberra"},
    {"id":"3","name":"USA","capital":"LA"},
]

nextCountryId = 4

def _find_next_id(id):
    data = [x for x in countries if x["id"]==id]
    return data

#GET - REST APIs
@app.route("/countries", methods=["GET"])
def get_country():
    return jsonify(countries)

#GET - by ID
@app.route("/countries/<id>", methods=["GET"])
def get_country_id(id):
    data = _find_next_id(id)
    return jsonify(data)

def get_country(id):
  return next((x for x in countries if x["id"] == id), None)

def country_is_valid(country):
  for key in country.keys():
    if key != "name":
      return False
  return True

@app.route("/countries", methods=["POST"])
def post_country():
    id = request.form.get("id")
    name = request.form.get("name")
    capital = request.form.get("capital")

    new_data = {
        "id": id,
        "name": name,
        "capital": capital
    }

    if (_find_next_id(id)):
        return {"error": "Bad Request"}, id
    else:
        countries.append(new_data)
        return jsonify(countries)

@app.route('/countries/<id>', methods=["PUT"])
def update_country(id):
    global countries
    name = request.form.get('name')
    capital = request.form.get('capital')
    update_data = {
        "name" : name,
        "capital" : capital
    }
    for country in countries:
        if id == country.get("id"):
            country["name"] = str(name)
            country["capital"] = str(capital)
            return jsonify(countries)
    else:
        return "Error", 404

@app.route('/countries/<id>', methods=["PATCH"])
def patch_country(id):
    name = request.form.get('name')
    capital = request.form.get('capital')
    update_data = {
        "name" : name,
        "capital" : capital
    }
    for country in countries:
        if id == country.get("id"):
            country["name"] = str(name)
            country["capital"] = str(capital)
            return jsonify(countries)
    else:
        return "Error", 404
        
@app.route('/countries/<id>', methods=['DELETE'])
def delete_country(id):
  global countries
  country = get_country(id)
  if country is None:
    return jsonify({ 'error': 'Country does not exist.' }), 404

  countries = [x for x in countries if x['id'] != id]
  return jsonify(" Successfully deleted country "), 200

if __name__ == "__main__" :
    app.run(host="0.0.0.0", port=5000, debug=True)