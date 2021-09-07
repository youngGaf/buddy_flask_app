from app import db
from flask import request, Blueprint
from ..models.FeatureVotesModel import FeaturesVotesSchema, FeaturesVotesModel
from ..models.UserModel import UserModel
from ..models.FeaturesModel import FeaturesModel
from ..utils.customResponse import custom_response

features_vote_api = Blueprint('votes', __name__)
features_vote_schema = FeaturesVotesSchema()


@features_vote_api.route('/action/<int:user_id>', methods=['POST'])
def vote_feature_action(user_id):
    """
    Feature vote action: vote and un-vote
    """
    req_data = request.get_json()
    feature_id = request.args.get('feature_id')

    # Check is user exist in db
    user_exists = UserModel.get_one_user(user_id)
    if not user_exists:
        return custom_response(
            {'message': 'Sorry voting aborted, user with User ID: %s does not exists' % user_id},
            400
        )

    # Check if feature exists
    feature_exists = FeaturesModel.get_one_feature(feature_id)
    if not feature_exists:
        return custom_response(
            {'message': 'Sorry voting aborted, feature with ID: %s does not exists' % feature_id},
            400
        )

    req_data['feature_id'] = feature_id
    req_data['user_id'] = user_id
    data = features_vote_schema.load(req_data)
    vote_exists = FeaturesVotesModel.query.filter_by(user_id=user_id,
                                                     feature_id=feature_id).first()

    # If vote exists carryout remove vote action
    if vote_exists:
        vote_exists.delete()
        return custom_response(
            {'message': 'Successfully removed vote'},
            200
        )

    # Add vote to db
    new_vote = FeaturesVotesModel(data)
    new_vote.save()
    return custom_response({'message': 'Voted successfully'}, 201)
