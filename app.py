from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os

# Init app
app = Flask(__name__)

# Database

# set configuration variables
DB_HOST = 'localhost'
DB_USERNAME = 'root'
DB_NAME = 'flask_db'

DB_MYSQL = f'mysql+pymysql://{DB_USERNAME}@{DB_HOST}:3306/{DB_NAME}'
DB_POSTGRES = f'postgresql://{DB_USERNAME}@{DB_HOST}:5432/{DB_NAME}'

app.config['SQLALCHEMY_DATABASE_URI'] = DB_MYSQL

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Init DB
db = SQLAlchemy(app)
# Init Marshmallow (Marshmallow is a Python library that is often used in Flask applications for object serialization and deserialization.)
ma = Marshmallow(app)

# Todo Class/Model
class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  description = db.Column(db.String(200))
  is_done = db.Column(db.String(1))

  def __init__(self, description, is_done):
    self.description = description
    self.is_done = is_done


# Todo Schema For Serialization
class TodoSchema(ma.Schema):
  class Meta:
    fields = ('id', 'description', 'is_done')
    

# Init schema
todo_schema = TodoSchema() # todo_schema is used for serializing a single Todo object
todos_schema = TodoSchema(many=True) # todos_schema is used for serializing a list of Todo objects


# Add Todo Endpoint
@app.route('/todos', methods=['POST'])
def add_todo():
  # read the description and is_done from the request body
  description = request.json['description'] 
  is_done = request.json['is_done']

  new_todo = Todo(description, is_done) # create a new Todo object

  db.session.add(new_todo) # add the new todo to the database session

  db.session.commit() # commit the changes to the database

  return todo_schema.jsonify(new_todo) # return the serialized version of the new todo object


# Get All Todos Endpoint
@app.route('/todos', methods=['GET'])
def get_todos():
  all_todos = Todo.query.all() # query all the todos from the database
  result = todos_schema.dump(all_todos) # serialize the todos into a JSON response
  return jsonify(result)


# Get Single Todo Endpoint
@app.route('/todos/<int:id>', methods=['GET'])
def get_todo_by_id(id):
  todo = Todo.query.get(id) # query the todo by id from the database
  return todo_schema.jsonify(todo) # serialize the todo into a JSON response


# Update Todo Endpoint
@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
  todo = Todo.query.get(id) # get the todo with the given ID from the database

  if not todo: # if the todo does not exist, return a 404 error
    return jsonify({'error': 'Todo not found'}), 404

  # update the todo object with the new data from the request body
  todo.description = request.json['description']
  todo.is_done = request.json['is_done']

  db.session.commit() # commit the changes to the database

  return todo_schema.jsonify(todo) # return the serialized version of the updated todo object


# Delete Todo Endpoint
@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
  todo = Todo.query.get(id) # retrieve the todo object by id
  db.session.delete(todo) # delete the todo object
  db.session.commit() # commit the changes to the database
  return todo_schema.jsonify(todo) # return the serialized version of the deleted todo object


# Run Server
if __name__ == '__main__':
    app.run(debug=True)