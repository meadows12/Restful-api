
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.store import StoreModel

datbase = "data.db"
class Store(Resource):
    
    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message":"Store not found"},404

    def post(self,name):
        if StoreModel.find_by_name(name):
            return {"message":"This item with name '{}' already exists.".format(name)},404

        store = StoreModel(name)
        
        try:
            store.save_todb()
        except Exception as e:
            return {"message":"An error occurred while inserting"},500
       
        return store.json(),201

    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_fromdb()

        return {"message":"Store deleted"}

    
        
    

class StoreList(Resource):
     def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]} # or list(map(lambda x:x.json(),ItemModel.query.all()))
    
