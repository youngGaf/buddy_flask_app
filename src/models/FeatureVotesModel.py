import datetime
from app import db
from marshmallow import fields, Schema


class FeaturesVotesModel(db.Model):
    """
    Features vote model
    """

    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)
    vote = db.Column(db.Boolean)
    feature_id = db.Column(db.Integer, db.ForeignKey('features.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime)

    def __init__(self, data):
        """
        Class constructor
        """
        self.vote = data.get('vote')
        self.feature_id = data.get('feature_id')
        self.user_id = data.get('user_id')
        self.created_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_votes():
        return FeaturesVotesModel.query.all()

    def __repr__(self):
        return '<id {}>'.format(self.id)


class FeaturesVotesSchema(Schema):
    """
    Features vote schema
    """
    id = fields.Int(dump_only=True)
    vote = fields.Boolean(required=True)
    feature_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)



