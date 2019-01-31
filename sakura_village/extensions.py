from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

ADMIN: Admin = Admin(template_mode='bootstrap3')
DB: SQLAlchemy = SQLAlchemy()
MIGRATE: Migrate = Migrate()

