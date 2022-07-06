from datetime import datetime

from . import DB, Bcrypt


class User(DB.Model):
    # Table Name
    __tablename__ = "users"

    # Column
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(128), nullable=False)
    email = DB.Column(DB.String(128), nullable=False, unique=True)
    password = DB.Column(DB.String(128), nullable=False)
    created_at = DB.Column(DB.DateTime)
    updated_at = DB.Column(DB.DateTime)

    def __init__(self, data):
        self.name = data.get("name")
        self.email = data.get("email")
        self.password = User.generate_hash(data.get('password'))
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @staticmethod
    def generate_hash(password):
        return Bcrypt.generate_password_hash(password=password, rounds=10).decode("utf-8")

    def check_hash(self, password):
        return Bcrypt.check_password_hash(pw_hash=self.password, password=password)

    def save(self):
        DB.session.add(self)
        DB.session.commit()

    @staticmethod
    def check_email(email):
        return User.query.filter_by(email=email).first()

