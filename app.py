from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "secret_key"

app.config.update(
    TESTING=True,
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/'
)

app.config['MONGO_URI'] = "mongodb://localhost:27017/flaskpymongo"

#Initialises PyMongo library
mongo = PyMongo(app)

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/')
def index():
    return jsonify('Hello World, I am here')

@app.route('/add', methods = ['POST'])
def add_user():
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['pwd']

    if _name and _email and _password and request.method == 'POST':
        _hashed_password = generate_password_hash(_password)

        id = mongo.db.user.insert({'name':_name, 'email': _email, 'pwd': _password})

        response = jsonify('User added successfully')

        response.status_code = 200

        return response

    else:
        return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found' + request.url
    }

    response = jsonify(message)

    response.status_code(404)

    return response