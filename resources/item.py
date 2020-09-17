
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

datbase = "data.db"
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type = float,
            required=True,
            help = "This field cannot be empty"
    )
    parser.add_argument('store_id',
            type = int,
            required=True,
            help = "Every items need a store id"
    )

    @jwt_required()
    def get(self,name):
        #  for item in items:
        #     if item['name'] == name:
        #         return item 
        # item = next(filter(lambda x : x['name']==name,items),None)
        # return {'item': item}, 200 if item else 404

        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message":"Item not found"}

    def post(self,name):
        if ItemModel.find_by_name(name):
            return {"message":"This item with name '{}' already exists.".format(name)},404

        data = Item.parser.parse_args()
        item = ItemModel(name,data['price'],data['store_id'])
        
        try:
            item.save_todb()
        except Exception as e:
            return {"message":"An error occurred while inserting"},500
       
        return item.json(),201

    def delete(self,name):
        #  global items
        # items = next(filter(lambda x: x['name']==name,items),None)
        # return {"message":"Item deleted"}
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_fromdb()

        return {"message":"Item deleted"}

    def put(self,name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        

        if item is None:
            item = ItemModel(name,data['price'],data['store_id'])
        else:
            item.price = data['price']
        
        item.save_todb()
        return item.json()
        
    

class ItemList(Resource):
     def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]} # or list(map(lambda x:x.json(),ItemModel.query.all()))
    
