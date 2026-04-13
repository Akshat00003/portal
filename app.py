from flask import Flask
app = None
from application.database import db
def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement_portal_database.sqlite3"
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()
from application.controllers import *

if __name__ == "__main__":
    with app.app_context():  
        db.create_all()
        admin = User.query.filter_by(role = "admin").first()
        if admin is None:
            admin = User(f_name = "admin" , l_name = "admin1" , username ="admin12" , email = "admin@user.com" , contact = "000000000" , password = "admin123" , role ="admin")
            db.session.add(admin)
            db.session.commit()
    app.run()






