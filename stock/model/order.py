import datetime as dt

from marshmallow import Schema, fields


class Order():
  def __init__(self, order_id, order_tag,symbol, quantity,filled_quantity,status):
    self.order_id = order_id
    self.order_tag = order_tag
    self.symbol = symbol
    self.quantity = quantity
    self.filled_quantity = filled_quantity
    self.status = status
    self.created_at = dt.datetime.now()
    

  def __repr__(self):
    return '<Order(name={self.description!r})>'.format(self=self)


class OrderSchema(Schema):
  order_id = fields.Str()
  order_tag = fields.Str()
  symbol = fields.Str()
  quantity = fields.Number()
  filled_quantity = fields.Number()
  status = fields.Str()
  created_at = fields.Date()