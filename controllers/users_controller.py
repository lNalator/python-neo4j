from flask import Blueprint, request, jsonify, abort
from services.users_service import UsersService
from resources.user_dto import CreateUserDto, UpdateUserDto

users_bp = Blueprint('users', __name__)
service = UsersService()

@users_bp.route('/', methods=['GET'])
def get_users():
    return jsonify(service.get_all_users())

@users_bp.route('/', methods=['POST'])
def create_user():
    json_data = request.get_json() or {}
    try:
        dto = CreateUserDto(**json_data)
    except TypeError:
        abort(400, "Missing required fields: name, email")
    if not isinstance(dto.email, str) or not isinstance(dto.content, str):
        abort(400, "Invalid data types")
    return jsonify(service.create_user(dto)), 201

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = service.get_user(user_id)
    if not user:
        abort(404)
    return jsonify(user)

@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    json_data = request.get_json() or {}
    dto = UpdateUserDto(**json_data)
    if not isinstance(dto.email, str) or not isinstance(dto.content, str):
        abort(400, "Invalid data types")
    updated = service.update_user(user_id, dto)
    if not updated:
        abort(404)
    return jsonify(updated)

@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    success = service.delete_user(user_id)
    if not success:
        abort(404)
    return jsonify({'success': True})

@users_bp.route('/<int:user_id>/friends', methods=['GET'])
def get_friends(user_id):
    return jsonify(service.get_friends(user_id))

@users_bp.route('/<int:user_id>/friends', methods=['POST'])
def add_friend(user_id):
    data = request.get_json() or {}
    if not isinstance(data.get('friendId'), int):
        abort(400, "Invalid data types")
    return jsonify(service.add_friend(user_id, data.get('friendId')))

@users_bp.route('/<int:user_id>/friends/<friend_id>', methods=['DELETE'])
def remove_friend(user_id, friend_id):
    return jsonify(service.remove_friend(user_id, friend_id))

@users_bp.route('/<int:user_id>/friends/<friend_id>', methods=['GET'])
def are_friends(user_id, friend_id):
    return jsonify(service.are_friends(user_id, friend_id))

@users_bp.route('/<int:user_id>/mutual-friends/<other_id>', methods=['GET'])
def mutual_friends(user_id, other_id):
    return jsonify(service.mutual_friends(user_id, other_id))
