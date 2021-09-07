from app import db
from flask import request, Blueprint
from ..models.FeaturesModel import FeaturesModel, FeaturesSchema
from ..models.UserModel import UserModel
from ..utils.customResponse import custom_response
from ..utils.voteChecker import add_vote_counts, set_user_vote

features_api = Blueprint('features', __name__)
features_schema = FeaturesSchema()


@features_api.route('/create/<int:user_id>', methods=['POST'])
def create_feature(user_id):
    """
    Create features
    """
    req_data = request.get_json()

    # Check is user exist in db
    user_exists = UserModel.get_one_user(user_id)
    if not user_exists:
        return custom_response(
            {'message': 'Cannot create feature, User with User ID: %s does not exists' % user_id},
            400
        )
    req_data['user_id'] = user_id
    data = features_schema.load(req_data)

    # Check if feature already exists
    feature_exists = FeaturesModel.query.filter_by(title=data.get('title')).all()
    if feature_exists:
        return custom_response(
            {'message': 'sorry this feature suggestion already exists'},
            400
        )

    # Save to db
    new_feature = FeaturesModel(data)
    new_feature.save()
    ser_feature = features_schema.dump(new_feature)
    return custom_response({
        'message': 'Successfully created feature',
        'data': ser_feature
        },
        201
    )


@features_api.route('/all/<int:user_id>', methods=['GET'])
def get_features(user_id):
    """
    Get all features
    """
    features = FeaturesModel.get_all_features()
    ser_features = features_schema.dump(features, many=True)
    update_ser_features = add_vote_counts(ser_features, user_id)
    return custom_response({
        'message': 'Successfully fetched all features',
        'data': update_ser_features
        },
        200
    )


@features_api.route('/<int:user_id>', methods=['GET'])
def get_feature(user_id):
    """
    Get a single feature
    """
    # Check if feature exists
    feature_id = request.args.get('feature_id')
    feature = FeaturesModel.get_one_feature(feature_id)
    if not feature:
        return custom_response(
            {'message': 'Feature with feature ID: %s does not exists' % feature_id},
            400
        )

    ser_features = features_schema.dump(feature)

    # Set vote count
    ser_features['votes'] = len(ser_features['user_votes'])
    set_user_vote(ser_features, user_id)
    return custom_response({
        'message': 'Successfully fetched feature',
        'data': ser_features
        },
        200
    )
