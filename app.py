from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#initializing db
db = SQLAlchemy(app)

#initialize marshmallow
ma = Marshmallow(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200),unique=False,nullable=False)
    is_done = db.Column(db.Boolean,unique=False,nullable=False,default=False)

    def __init__(self,task,is_done):
        self.task = task
        self.is_done = is_done

class TodoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Todo
        load_instance = True

todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)

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


@app.route('/home', methods=['GET'])
def home():
    return {'respone':'hello world'}

if __name__ == '__main__':
    app.run()