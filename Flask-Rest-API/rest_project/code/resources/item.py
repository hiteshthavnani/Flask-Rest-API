from flask import request
from flask_restful import Resource
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):

    @jwt_required()
    def get(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'An item for name %s not found' % name}, 404


    def post(self, name):

        if ItemModel.find_by_name(name):
            return {'message': 'An item with name %s already exists' % name}, 400

        data = request.get_json()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting an item'}, 500
        return item.json(), 201

    def put(self, name):

        data = request.get_json()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()

    def delete(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}

        return {'message': 'An item cannot be deleted as name %s does not exist' %name}


class ItemList(Resource):

    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}