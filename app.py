from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)

stores = [
    {
        'name': 'My store',
        'items': [
            {
                'name': 'My item',
                'price': 25
            }
        ]
    }
]

@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data.get('name'),
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)

@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store.get('name') == name:
            return jsonify(store)
    return jsonify({'message': 'store not found'})

@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})


@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store.get('name') == name:
            new_item = {
                'name': request_data.get('name'),
                'price': request_data.get('price')
            }
            store.get('items').append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'store not found'})

@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    for store in stores:
        if store.get('name') == name:
            return jsonify(store.get('items'))
    return jsonify({'message': 'item not found'})

app.run(port=5000)
