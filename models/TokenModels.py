from datetime import datetime

from . import DB


class Token(DB.Model):
    # Define Table Name
    __tablename__ = "token"

    # Define Column
    id = DB.Column(DB.Integer, primary_key=True)
    token = DB.Column(DB.String(), nullable=False, unique=True)
    created_at = DB.Column(DB.DateTime)
    updated_at = DB.Column(DB.DateTime)

    # Create Constructor
    def __init__(self, token):
        self.token = token
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    # To Handle Save Data to Database
    def save(self):
        DB.session.add(self)
        DB.session.commit()

    # To Check if Token already in Database
    @staticmethod
    def check_token(token):
        return Token.query.filter_by(token=str(token)).first()
