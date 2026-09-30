from flask import Flask
from flask_jwt_extended import JWTManager
from application.config import LocalDevelopmentConfig
from application.database import db
from application.models import *
from application.security import jwt
from flask_cors import CORS
from application.celery_init import celery_init_app
app = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    JWTManager(app)
    CORS(app)
    app.app_context().push()
    return app

app = create_app()
celery = celery_init_app(app)
# celery.autodiscover_tasks()

from application import tasks
from application.routes import *


with app.app_context():
    db.create_all()
    if not User.query.filter_by(username = 'admin').first():
        print("Creating admin user...")
        admin_user = User(username = 'admin', role = 'admin')
        admin_user.set_password('AdminPassword123')
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")
        

if __name__ == "__main__":
    app.run(debug = True)