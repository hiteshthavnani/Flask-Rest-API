from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'A store with name %s already exists' % name}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occur creating a new user %s' %name}, 500
        return store.json(), 200

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': 'A store %s is successfully deleted' % name}, 200

        return {'message': 'An error occur while deleting a user %s' % name}, 500


class StoreList(Resource):

    def get(self):
        return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}