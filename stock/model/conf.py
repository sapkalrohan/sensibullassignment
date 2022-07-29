import os
#from flask import Flask,jsonify, request
from quart import Quart, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Quart(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir, 'db.sqlite3')
db = SQLAlchemy(app)

def setup_routes():
    from stock.model.order import OrderModel, OrderSchema  
    #db.drop_all()
    db.create_all()
    
    """          
    "order": {
        "filled_quantity": 0,
        "order_id": "6d3e9f00-2f00-4e6d-ad42-f6d12df7c0b9",
        "order_tag": "yyyyyy",
        "request_quantity": 11,
        "status": "open",
        "symbol": "HDFC"
    }
    dummyorders = [
      OrderSchema().load({
        "filled_quantity": 0,
        "order_id": "6d3e9f00-2f00-4e6d-ad42-f6d12df7c0b9",
        "order_tag": "yyyyyy",
        "request_quantity": 11,
        "status": "open",
        "symbol": "HDFC"
        })
    ]
    for o in dummyorders:
        db.session.add(OrderModel(**o))
    
    db.session.commit()
    """

    orders_schema = OrderSchema(many=True)
    order_schema = OrderSchema()

    @app.route('/order-service/status')
    async def get_orderstatus():
      all_orders = OrderModel.query.all()
      return jsonify(orders_schema.dump(all_orders))


    @app.route('/order-service', methods=['POST'])
    async def place_order():
        result = await OrderModel.create(await request.get_json())
        if(type(result) is str):
            return jsonify({
                "success": False,
                "err_msg": result
                }), 500
        return jsonify({
            "success": True,
            "payload": result
            }), 200
        



    @app.route('/order-service', methods=['PUT'])
    def modify_order():
      json = request.get_json()
      order = OrderSchema().load(json)
      return "", 204



    @app.route('/order-service', methods=['DELETE'])
    def delete_order():
      json = request.get_json()
      order = OrderSchema().load(json)
      return "", 204