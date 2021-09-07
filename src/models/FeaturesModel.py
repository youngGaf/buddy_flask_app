import datetime
from app import db
from marshmallow import fields, Schema
from .FeatureVotesModel import FeaturesVotesSchema, FeaturesVotesModel


class FeaturesModel(db.Model):
    """
    Features model
    """

    # table name
    __tablename__ = 'features'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    details = db.Column(db.String(300), nullable=False)
    votes = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    user_votes = db.relationship('FeaturesVotesModel', backref='features', lazy=True)

    def __init__(self, data):
        """
        Class constructor
        :param data:
        """
        self.title = data.get('title')
        self.details = data.get('details')
        self.votes = data.get('votes')
        self.user_id = data.get('user_id')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_features():
        return FeaturesModel.query.all()

    @staticmethod
    def get_one_feature(feature_id):
        return FeaturesModel.query.get(feature_id)

    def get_vote_count(self):
        return FeaturesVotesModel.query.filter_by(features_id=self.feature_id).count()

    def __repr__(self):
        return '<id {}>'.format(self.id)


class FeaturesSchema(Schema):
    """
    Features schema
    """
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    details = fields.Str(required=True)
    votes = fields.Int(required=True)
    user_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    user_votes = fields.Nested(FeaturesVotesSchema, many=True)
