from flask import Flask, request, jsonify
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config.from_object("config.Config")

from models import db ,Todo, todos_schema, todo_schema



@app.route('/todo', methods=['GET'])
def get_todos():
    all_todos = Todo.query.all()
    results = todos_schema.dump(all_todos)
    return jsonify(results)

@app.route('/todo/<id>', methods=['GET'])
def get_todo(id):
    todo = Todo.query.get(id)
    result = todo_schema.dump(todo)
    return jsonify(result)

@app.route('/todo/<id>', methods=['PUT'])
def put_todo(id):
    todo = Todo.query.get(id)
    todo.task = request.json['task']
    todo.is_done = request.json['is_done']
    db.session.commit()
    result = todo_schema.dump(todo)
    return jsonify(result)

@app.route('/todo', methods=['POST'])
def post_todo():
    task = request.json['task']
    is_done = request.json['is_done']
    new_todo = Todo(task, is_done)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(todo_schema.dump(new_todo))

@app.route('/todo/<id>', methods=['DELETE'])
def delete_todo(id):
   todo = Todo.query.get(id)
   print(vars(todo))
   db.session.delete(todo)
   db.session.commit()
   return jsonify(todo_schema.dump(todo))


@app.route('/', methods=['GET'])
def home():
    return {'respone':'hello world'}

if __name__ == '__main__':
    app.run()