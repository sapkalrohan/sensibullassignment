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
  request_quantity = db.Column(db.Integer,nullable=False)
  filled_quantity = db.Column(db.Integer)
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
  
  def get(identifier):
    return OrderModel.query.get(identifier)
  
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
    
  async def statusupdate():
      try:
        print('getting order status updates from sensibull api')
        openorders = OrderModel.query.filter_by(status='open').all()
        if openorders.__len__() < 1:
          print('NO Open orders to get status updates from sensibull api,DONE')
          return True
        sensibull_response = await SensibullApis.status([o.order_id for o in openorders])
        openorders = {x.order_id: x for x in openorders}
        if isinstance( sensibull_response ,  Exception):
          return str(sensibull_response)
        elif sensibull_response['success'] == False:
          return sensibull_response['err_msg']
        elif sensibull_response['success'] is True:
          for order in sensibull_response['payload']:
            ordertoupdate = openorders[order["order_id"]]
            ordertoupdate.status = order["status"]
            ordertoupdate.filled_quantity = order["filled_quantity"]
            ordertoupdate.updated_at = dt.datetime.now()
            db.session.add(ordertoupdate)
        db.session.commit()
        print('DONE getting order status updates from sensibull api')
        return True
      except Exception as e:
        error = str(e)
        return error
    
  async def modify(order_id,quantity):
    try:
      schema = OrderSchema()
      sensibull_response = await SensibullApis.modify(order_id,quantity)
      if isinstance( sensibull_response ,  Exception):
        return str(sensibull_response)
      elif sensibull_response['success'] == False:
        return sensibull_response['err_msg']
      
      modifiedorder = sensibull_response['payload']['order']
      localorder = OrderModel.query.get(order_id)
      localorder.request_quantity = modifiedorder['request_quantity']
      localorder.status = modifiedorder['status']
      localorder.updated_at = dt.datetime.now()
      db.session.add(localorder)
      db.session.commit()
      
      orderschema = schema.dump(localorder)
      del orderschema["created_at"]
      del orderschema["updated_at"]
      return orderschema
    except Exception as e:
      error = str(e)
      return error

  async def cancel(order_id):
    try:
      schema = OrderSchema()
      sensibull_response = await SensibullApis.cancel(order_id)
      if isinstance( sensibull_response ,  Exception):
        return str(sensibull_response)
      elif sensibull_response['success'] == False:
        return sensibull_response['err_msg']
      
      modifiedorder = sensibull_response['payload']['order']
      localorder = OrderModel.query.get(order_id)
      localorder.request_quantity = modifiedorder['request_quantity']
      localorder.status = modifiedorder['status']
      localorder.updated_at = dt.datetime.now()
      db.session.add(localorder)
      db.session.commit()
      
      orderschema = schema.dump(localorder)
      del orderschema["created_at"]
      del orderschema["updated_at"]
      return orderschema
    except Exception as e:
      error = str(e)
      return error