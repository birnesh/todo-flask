from __main__ import app
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy(app)

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