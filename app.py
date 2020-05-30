from flask import Flask, request, jsonify
import os , uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config.from_object("config.Config")


db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

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

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True


todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

###########################  User api's  #############################

# List all user
@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()
    results = users_schema.dump(users)
    return jsonify(results)
    
# List a user
@app.route('/user/<public_id>', methods=['GET'])
def get_one_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message':'No user found!'})
    result = user_schema.dump(user)
    return jsonify(result)

# Delete a user
@app.route('/user<public_id>', methods=['DELETE'])
def delete_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message':'No user found!'})
    db.session.delete(user)
    db.session.commit()
    return jsonify(user_schema.dump(user))

# Make a user a admin user
@app.route('/user/<public_id>', methods=['PUT'])
def promote_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message':'No user found!'})
    user.admin = True
    db.session.commit()
    return jsonify({'message':'The User has been promoted!'})


# create user
@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method = 'sha256')
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'New User Created'})

###########################  todo api's  ##################################
# List all todos
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