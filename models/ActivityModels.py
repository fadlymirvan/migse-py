from datetime import datetime

from sqlalchemy import cast, Date, and_, between, func

from . import DB


class Activity(DB.Model):
    # Table Name
    __tablename__ = "activity"

    # Column
    id = DB.Column(DB.Integer, primary_key=True)
    user_id = DB.Column(DB.Integer, nullable=False)
    title = DB.Column(DB.String(25), nullable=False)
    description = DB.Column(DB.String(), nullable=False)
    created_at = DB.Column(DB.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = DB.Column(DB.DateTime, default=datetime.utcnow)

    def __init__(self, data):
        self.title = data.get("title")
        self.description = data.get("description")
        self.user_id = data.get("user_id")
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def update(self, data):
        self.title = data.title
        self.description = data.description
        self.user_id = data.user_id
        self.updated_at = datetime.utcnow()
        DB.session.commit()

    def save(self):
        DB.session.add(self)
        DB.session.commit()

    def delete(self):
        DB.session.delete(self)
        DB.session.commit()

    @staticmethod
    def get_all_activity(uid, date):
        return Activity.query.filter(
            and_(
                between(func.date(Activity.created_at), date, date),
                Activity.user_id == uid
            )
        ).all()

    @staticmethod
    def get_activity_by_id(aid):
        return Activity.query.filter_by(id=aid).first()

    @staticmethod
    def get_date_activity(uid):
        return DB.session.query(
            cast(Activity.created_at, Date)
        ).distinct().filter_by(
            user_id=uid
        ).all()
