from app import db
from flask import request, Blueprint
from ..models.UserModel import UserModel, UsersSchema
from ..utils.customResponse import custom_response


user_api = Blueprint('users', __name__)
user_schema = UsersSchema()


@user_api.route('/create', methods=['POST'])
def create_user():
    """
    Create user
    """
    req_data = request.get_json()
    data = user_schema.load(req_data)
    user_exists = UserModel.query.filter_by(name=data.get('name')).all()

    if user_exists:
        return custom_response(
            {'message': 'sorry this user already exists'},
            400
        )

    # Save to db
    new_user = UserModel(data)
    new_user.save()
    return custom_response({'message': 'Successfully created user'}, 201)


@user_api.route('/all', methods=['GET'])
def get_users():
    """
    Get all users
    """
    users = UserModel.get_all_users()
    ser_users = user_schema.dump(users, many=True)
    return custom_response({
        'message': 'Successfully fetched all users',
        'data': ser_users
        },
        200
    )


@user_api.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get a single user
    """
    user = UserModel.get_one_user(user_id)
    if not user:
        return custom_response(
            {'message': 'User with User ID: %s does not exists' % user_id},
            400
        )

    ser_user = user_schema.dump(user)
    return custom_response({
        'message': 'Successfully fetched feature',
        'data': ser_user
        },
        200
    )


@user_api.route('/delete', methods=['DELETE'])
def delete_user():
    """
    Delete a user
    :param
    user_id
    """
    user_id = request.args.get('user_id')
    user = UserModel.get_one_user(user_id)

    if not user:
        return custom_response(
            {'message': 'User with User ID: %s does not exists' % user_id},
            400
        )

    user.delete()
    return custom_response({'message': 'Successfully deleted user'}, 200)
