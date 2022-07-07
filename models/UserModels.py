from datetime import datetime

from . import DB, Bcrypt


class User(DB.Model):
    # Define Table Name
    __tablename__ = "users"

    # Define Column
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(128), nullable=False)
    email = DB.Column(DB.String(128), nullable=False, unique=True)
    password = DB.Column(DB.String(128), nullable=False)
    created_at = DB.Column(DB.DateTime)
    updated_at = DB.Column(DB.DateTime)

    # Create Constructor
    def __init__(self, data):
        self.name = data.get("name")
        self.email = data.get("email")
        self.password = User.generate_hash(data.get('password'))
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    # Generate Hashed Password
    @staticmethod
    def generate_hash(password):
        return Bcrypt.generate_password_hash(password=password, rounds=10).decode("utf-8")

    # To Check if Hashed Password is Same
    def check_hash(self, password):
        return Bcrypt.check_password_hash(pw_hash=self.password, password=password)

    # To Save data to Database
    def save(self):
        DB.session.add(self)
        DB.session.commit()

    # To Handle Get Data by Email
    @staticmethod
    def check_email(email):
        return User.query.filter_by(email=email).first()

