import os

from flask import Flask
from flask_pymongo import PyMongo
from flask import jsonify
from flask import request


app = Flask(__name__)

user = os.environ.get('MONGO_USER')
password = os.environ.get('MONGO_PASSWORD')
url_mongo = os.environ.get('MONGO_URL')

app.config['MONGO_DBNAME'] = 'Cars'
app.config['MONGO_URI'] = 'mongodb://'+user+':'+password+'@'+url_mongo+'/dsd-mongo'

mongo = PyMongo(app)


@app.route('/manufacturer', methods=['GET'])
def get_all_manufacturers():
    cars = mongo.db.Cars
    output = []
    for s in cars.find():
        output.append({'manufacturer': s['manufacturer'], 'model': s['model']})
    return jsonify({'result': output})


@app.route('/manufacturer/<manufacturer>', methods=['GET'])
def get_one_manufacturer(manufacturer):
    cars = mongo.db.Cars
    s = cars.find_one({'manufacturer': manufacturer})
    if s:
        output = ({'manufacturer': s['manufacturer'], 'model': s['model']})
    else:
       output = "No such name"
    return jsonify({'result' : output})


@app.route('/manufacturer', methods=['POST'])
def add_manufacturer():
    cars = mongo.db.Cars
    manufacturer = request.json['manufacturer']
    model = request.json['model']
    cars_id = cars.insert({'manufacturer': manufacturer, 'model': model})
    new_manufacturer = cars.find_one({'_id': cars_id })
    output = {'manufacturer' : new_manufacturer['manufacturer'], 'manufacturer' : new_manufacturer['model']}
    return jsonify({'result' : output})


if __name__ == '__main__':
    app.run(debug=True)
