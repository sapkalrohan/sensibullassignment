from flask_sqlalchemy import SQLAlchemy
import os

class Database():
  _instance = None
  
  @staticmethod
  def getInstance():
      """Static Access Method"""
      if Database._instance == None:
          Database()
      return Database._instance

  def __init__(self):
      """virtual private constructor"""
      
      if Database._instance != None:
          raise Exception("tried to init database again")
      else:
          from .conf import app
          basedir = os.path.abspath(os.path.dirname(__file__))
          app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir, 'db.sqlite3')
          self.db = SQLAlchemy(app)
          Database._instance = self
            
  def __repr__(self):
    return '<Database(name=database)>'
