from flask import Flask
from flask_migrate import Migrate

from utils import Config
from routes import authRoutes, activityRoutes, attendanceRoutes
from models import DB, Bcrypt

app = Flask(__name__)
app.config.from_object(Config)
Bcrypt.init_app(app)
DB.init_app(app)

Migrate(app, DB)


PREFIX = "/api/v1"
app.register_blueprint(authRoutes, url_prefix=PREFIX+'/auth')
app.register_blueprint(activityRoutes, url_prefix=PREFIX+'/activity')
app.register_blueprint(attendanceRoutes, url_prefix=PREFIX+'/attendance')


if __name__ == '__main__':
    app.run()
