import random, uuid
import datetime as dt
from .conf import db
from marshmallow import Schema, fields
from .sensibullapis import SensibullApis

class OrderSchema(Schema):
  order_id = fields.Str()
  order_tag = fields.Str()
  symbol = fields.Str()
  request_quantity = fields.Integer()
  filled_quantity = fields.Integer()
  status = fields.Str()
  created_at = fields.DateTime()
  updated_at = fields.DateTime()

class OrderModel(db.Model):
  order_id = db.Column(db.String(255), primary_key=True)
  order_tag = db.Column(db.String(255),nullable=False)
  symbol = db.Column(db.String(255),nullable=False)
  request_quantity = db.Column(db.Numeric,nullable=False)
  filled_quantity = db.Column(db.Numeric)
  status = db.Column(db.String(255),nullable=False)
  created_at = db.Column(db.DateTime,default=dt.datetime.now(),nullable=False)
  updated_at = db.Column(db.DateTime,default=dt.datetime.now(),nullable=True)
    
  def __init__(self, order_id, order_tag,symbol, request_quantity,filled_quantity,status):
    self.order_id = order_id
    self.order_tag = order_tag
    self.symbol = symbol
    self.request_quantity = request_quantity
    self.filled_quantity = filled_quantity
    self.status = status
    self.created_at = dt.datetime.now()
    self.updated_at = dt.datetime.now()
    
  def __repr__(self):
    return f'<OrderModel {self.order_id}>'
  
  async def create(json):
    try:
      schema = OrderSchema()
      orderschema = schema.load(json)
      orderschema["order_tag"] = "yyyyyy"
      
      sensibull_response = await SensibullApis.create(orderschema["symbol"],orderschema["request_quantity"],orderschema["order_tag"])
      if isinstance( sensibull_response ,  Exception):
        return str(sensibull_response)
      elif sensibull_response['success'] == False:
        return sensibull_response['err_msg']
      
      orderschema["order_id"] = sensibull_response['payload']['order']['order_id'] #WILL GET FROM API
      orderschema["filled_quantity"] = sensibull_response['payload']['order']['filled_quantity']
      orderschema["status"] = sensibull_response['payload']['order']['status'] #WILL GET FROM API
      order = OrderModel(**orderschema)
      db.session.add(order)
      db.session.commit()
      orderschema = schema.dump(order)
      del orderschema["created_at"]
      del orderschema["updated_at"]
      return orderschema
    except Exception as e:
      error = str(e)
      return error
