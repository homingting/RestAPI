import uuid
from sqlalchemy.exc import SQLAlchemyError , IntegrityError
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from schemas import StoreSchema,PlainStoreSchema
from db import db
from models import StoreModel

blp = Blueprint("stores",__name__,description="Operation on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200,StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
    
    def delete(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message":"The store deleted."},202
            
@blp.route("/store")
class storeslist(MethodView):
    @blp.response(201,StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @blp.arguments(StoreSchema)
    @blp.response(200,StoreSchema)
    def post(self,store_data):   
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400,message="A store with that name already exists.",)
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.",)
        return store