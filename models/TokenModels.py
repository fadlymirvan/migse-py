from datetime import datetime

from . import DB


class Token(DB.Model):
    # Table Name
    __tablename__ = "token"

    # Column
    id = DB.Column(DB.Integer, primary_key=True)
    token = DB.Column(DB.String(), nullable=False, unique=True)
    created_at = DB.Column(DB.DateTime)
    updated_at = DB.Column(DB.DateTime)

    def __init__(self, token):
        self.token = token
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def save(self):
        DB.session.add(self)
        DB.session.commit()

    @staticmethod
    def check_token(token):
        return Token.query.filter_by(token=str(token)).first()
