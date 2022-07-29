from operator import is_not
import os,asyncio
from quart import Quart, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from quart_schema import QuartSchema, validate_request
from dataclasses import dataclass, asdict
from typing import Optional

app = Quart(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "db.sqlite3"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

from stock.model.order import OrderModel, OrderSchema

##POLLING BACKGROUND JOB
async def schedule():
    while True:
        await asyncio.sleep(15)
        await OrderModel.statusupdate()

@app.before_serving
async def startup():
    app.add_background_task(schedule)
##

orders_schema = OrderSchema(many=True)
order_schema = OrderSchema()

def convert_to_localdto(orderdto):
    if isinstance(orderdto, OrderModel):
        orderdto = order_schema.dump(orderdto)
    if orderdto is None:
        return None
    orderdto["identifier"] = orderdto["order_id"]
    orderdto["quantity"] = orderdto["request_quantity"]
    orderdto["order_status"] = orderdto["status"]
    del (
        orderdto["order_tag"],
        orderdto["order_id"],
        orderdto["request_quantity"],
        orderdto["status"],
    )
    if "updated_at" in orderdto:
        del orderdto["updated_at"]
    if "created_at" in orderdto:
        del orderdto["created_at"]
    return {"success": True, "payload": orderdto}

@dataclass
class Order:
    identifier: str
    new_quantity: Optional[int] = None


@dataclass
class CreateOrder:
    symbol: str
    quantity: int

QuartSchema(app)

def setup_routes():
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

    @app.route("/order-service/all")
    async def get_allorders():
        all_orders = OrderModel.query.all()
        return jsonify(orders_schema.dump(all_orders))
    
    @app.route("/order-service/statusupdate")
    async def get_allorderstatus():
        all_orders = await OrderModel.statusupdate()
        return "", 200

    @app.route("/order-service/status", methods=["POST"])
    @validate_request(Order)
    async def get_orderstatus(data: Order):
        order = OrderModel.get(data.identifier)
        if order is None:
            return jsonify({"success": False, "err_msg": "not found"}), 404
        return jsonify(convert_to_localdto(order)), 200

    @app.route("/order-service", methods=["POST"])
    @validate_request(CreateOrder)
    async def place_order(data: CreateOrder):
        data = asdict(data)
        data["request_quantity"] = data["quantity"]
        del data["quantity"]
        result = await OrderModel.create(data)
        if type(result) is str:
            return jsonify({"success": False, "err_msg": result}), 500
        return jsonify(convert_to_localdto(result)), 200

    @app.route("/order-service", methods=["PUT"])
    @validate_request(Order)
    async def modify_order(data: Order):
        result = await OrderModel.modify(data.identifier, data.new_quantity)
        if type(result) is str:
            return jsonify({"success": False, "err_msg": result}), 500
        return jsonify(convert_to_localdto(result)), 200

    @app.route("/order-service", methods=["DELETE"])
    @validate_request(Order)
    async def delete_order(data: Order):
        result = await OrderModel.cancel(data.identifier)
        if type(result) is str:
            return jsonify({"success": False, "err_msg": result}), 500
        return jsonify(convert_to_localdto(result)), 200
