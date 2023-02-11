from flask import Flask, jsonify, abort, make_response, request
from models import bookslibrary

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"


@app.route("/api/v1/bookslibrary/", methods=["GET"])
def bookslibrary_list_api_v1():
  return jsonify(bookslibrary.all())


@app.route("/api/v1/bookslibrary/<int:book_id>/", methods=["GET"])
def get_book(book_id):
  namebook = bookslibrary.get(book_id)
  if not namebook:
    abort(404)
  return jsonify({"namebook": namebook})


@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)


@app.route("/api/v1/bookslibrary/", methods=["POST"])
def create_book():
  if not request.json or not 'namebook' in request.json:
    abort(400)
  namebook = {
      'id': bookslibrary.all()[-1]['id'] + 1,
      'namebook': request.json['namebook'],
      'author': request.json['author'],
      'yearbook': request.json['yearbook'],
      'coverimage': request.json['coverimage'],      
      'description': request.json.get('description', "")
  }
  bookslibrary.create(namebook)
  return jsonify({'namebook': namebook}), 201


@app.route("/api/v1/bookslibrary/<int:book_id>", methods=['DELETE'])
def delete_book(book_id):
  result = bookslibrary.delete(book_id)
  if not result:
    abort(404)
  return jsonify({'result': result})


@app.route("/api/v1/bookslibrary/<int:book_id>", methods=["PUT"])
def update_book(book_id):
  namebook = bookslibrary.get(book_id)
  if not namebook:
    abort(404)
  if not request.json:
    abort(400)
  data = request.json
  if any([
      'namebook' in data and not isinstance(data.get('namebook'), str),
      'author' in data and not isinstance(data.get('author'), str),
      'yearbook' in data and not isinstance(data.get('yearbook'), str),
      'coverimage' in data and not isinstance(data.get('coverimage'), str),
      'description' in data and not isinstance(data.get('description'), str)
  ]):
    abort(400)
  namebook = {
      'namebook': data.get('title', namebook['namebook']),
      'author': data.get('title', namebook['author']),
      'yearbook': data.get('title', namebook['yearbook']),
      'coverimage': data.get('title', namebook['coverimage']),
      'description': data.get('description', namebook['description'])
  }
  bookslibrary.update(book_id, namebook)
  return jsonify({'namebook': namebook})


@app.errorhandler(400)
def bad_request(error):
  return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


if __name__ == "__main__":
  app.run(debug=True)
