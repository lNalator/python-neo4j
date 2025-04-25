from flask import Blueprint, request, jsonify, abort
from services.comments_service import CommentsService
from resources.comment_dto import UpdateCommentDto


comments_bp = Blueprint('comments', __name__)
service = CommentsService()

@comments_bp.route('/', methods=['GET'])
def get_comments():
    return jsonify(service.get_all_comments())

@comments_bp.route('/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    return jsonify(service.get_comment(comment_id))

@comments_bp.route('/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    json_data = request.get_json() or {}
    dto = UpdateCommentDto(**json_data)
    if not isinstance(dto.user_id, int) or not isinstance(dto.content, str):
        abort(400, "Invalid data types")
    return jsonify(service.update_comment(comment_id, dto))

@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
def delete_comment_only(comment_id):
    return jsonify(service.comment_delete_only(comment_id))

@comments_bp.route('/<int:comment_id>/like', methods=['POST'])
def like_comment(comment_id):
    data = request.get_json() or {}
    return jsonify(service.like_comment(comment_id, data.get('userId')))

@comments_bp.route('/<int:comment_id>/like', methods=['DELETE'])
def unlike_comment(comment_id):
    data = request.get_json() or {}
    return jsonify(service.unlike_comment(comment_id, data.get('userId')))
