from datetime import datetime

from . import DB


class Attendance(DB.Model):
    # Table Name
    __tablename__ = "attendance"

    # Column
    id = DB.Column(DB.Integer, primary_key=True)
    user_id = DB.Column(DB.Integer, nullable=False)
    description = DB.Column(DB.String(15))
    created_at = DB.Column(DB.DateTime)
    updated_at = DB.Column(DB.DateTime)

    def __init__(self):
        self.user_id = ""
        self.description = ""
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def save(self):
        DB.session.add(self)
        DB.session.commit()

    @staticmethod
    def get_all_attendance(user_id):
        return Attendance.query.filter_by(user_id=user_id).all()
