from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

DB = SQLAlchemy()
Bcrypt = Bcrypt()

from .UserModels import User
from .ActivityModels import Activity
from .AttendanceModels import Attendance
from .TokenModels import Token
