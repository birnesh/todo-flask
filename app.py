from flask import Flask, request, jsonify, make_response
import os , uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import jwt
import datetime
from functools import wraps

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

# login required decorator
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token :
            return jsonify({'message':'Token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message':'Token is invalid!'}), 401
        return f(current_user,*args, **kwargs)
    return decorated

###########################  User api's  #############################

# List all user
@app.route('/user', methods=['GET'])
@login_required
def get_all_users(current_user):
    if not current_user.admin:
        return jsonify({'message':'Cannot perform this action!'})
    users = User.query.all()
    results = users_schema.dump(users)
    return jsonify(results)
    
# List a user
@app.route('/user/<public_id>', methods=['GET'])
@login_required
def get_one_user(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message':'No user found!'})
    result = user_schema.dump(user)
    return jsonify(result)

# Delete a user
@app.route('/user/<public_id>', methods=['DELETE'])
@login_required
def delete_user(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message':'No user found!'})
    db.session.delete(user)
    db.session.commit()
    return jsonify(user_schema.dump(user))

# Make a user a admin user
@app.route('/user/<public_id>', methods=['PUT'])
@login_required
def promote_user(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message':'No user found!'})
    user.admin = True
    db.session.commit()
    return jsonify({'message':'The User has been promoted!'})


# create user
@app.route('/user', methods=['POST'])
@login_required
def create_user(current_user):
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method = 'sha256')
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'New User Created'})

# Login user
@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify1', 401, {'WWW-Authenticate':'Basic realm-"Login required"'})
    user = User.query.filter_by(name=auth.username).first()
    if not user:
        return make_response('could not verify2', 401, {'WWW-Authenticate':'Basic realm-"Login required"'})
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id':user.public_id, 'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})
    return make_response('could not verify3', 401, {'WWW-Authenticate':'Basic realm-"Login required"'})

###########################  todo api's  ##################################
# List all todos
@app.route('/todo', methods=['GET'])
@login_required
def get_todos(current_user):
    all_todos = Todo.query.all()
    results = todos_schema.dump(all_todos)
    return jsonify(results)

@app.route('/todo/<id>', methods=['GET'])
@login_required
def get_todo(current_user, id):
    todo = Todo.query.get(id)
    result = todo_schema.dump(todo)
    return jsonify(result)

@app.route('/todo/<id>', methods=['PUT'])
@login_required
def put_todo(current_user, id):
    todo = Todo.query.get(id)
    todo.task = request.json['task']
    todo.is_done = request.json['is_done']
    db.session.commit()
    result = todo_schema.dump(todo)
    return jsonify(result)

@app.route('/todo', methods=['POST'])
@login_required
def post_todo(current_user):
    task = request.json['task']
    is_done = request.json['is_done']
    new_todo = Todo(task, is_done)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(todo_schema.dump(new_todo))

@app.route('/todo/<id>', methods=['DELETE'])
@login_required
def delete_todo(current_user, id):
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