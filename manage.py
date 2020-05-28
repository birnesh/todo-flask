# from flask_script import Manager
# from flask_migrate import Migrate, MigrateCommand

# # from flask.cli import FlaskGroup

# from app import app, db, Todo

# migrate = Migrate(app, db)
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

# # cli = FlaskGroup(app)

# # @cli.command("create_db")
# # def create_db():
# #     db.drop_all()
# #     db.create_all()
# #     db.session.commit()

# # @cli.command("seed_db")
# # def seed_db():
# #     db.session.add(Todo(task="michael@mherman.org", is_done=False))
# #     db.session.commit()




# if __name__ == "__main__":
#     manager.run()