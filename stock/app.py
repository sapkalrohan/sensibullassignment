import os
from flask import Flask, jsonify, request
from stock.model.order import Order, OrderSchema

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ \
                os.path.join(basedir, 'db.sqlite3')
      
"""          
"order": {
            "order_id": "9d05036f-b234-4856-8b2c-64a4764cd3d9",
            "order_tag": "yyyyyy",
            "symbol": "HDFC",
            "request_quantity": 10,
            "filled_quantity": 0,
            "status": "open"
        }
"""

orders = [
  Order('9d05036f-b234-4856-8b2c-64a4764cd3d9','yyyyyy','HDFC',10,0,'open')
]


@app.route('/order-service/status')
def get_orderstatus():
  schema = OrderSchema(many=True)
  data = schema.dump(orders)
  return jsonify(data)


@app.route('/order-service', methods=['POST'])
def place_order():
  json = request.get_json()
  print(json)
  json['quantity'] = json['request_quantity']
  json.pop('request_quantity')
  income = OrderSchema().load(json)
  orders.append(income)
  return "", 204


@app.route('/order-service', methods=['PUT'])
def modify_order():
  json = request.get_json()
  income = OrderSchema().load(json)
  orders.append(income)
  return "", 204



@app.route('/order-service', methods=['DELETE'])
def delete_order():
  json = request.get_json()
  income = OrderSchema().load(json)
  orders.append(income)
  return "", 204


if __name__ == "__main__":
    app.run()