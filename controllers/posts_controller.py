from flask import Blueprint, request, jsonify, abort
from services.posts_service import PostsService
from services.comments_service import CommentsService
from resources.post_dto import CreatePostDto, UpdatePostDto
from resources.comment_dto import CreateCommentDto

posts_bp = Blueprint('posts', __name__)
service = PostsService()
commentsService = CommentsService()

@posts_bp.route('/', methods=['GET'])
def get_posts():
    return jsonify(service.get_all_posts())

@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    p = service.get_post(post_id)
    if not p:
        abort(404)
    return jsonify(p)

@posts_bp.route('/by-user/<int:user_id>', methods=['GET'])
def get_user_posts(user_id):
    return jsonify(service.get_posts_by_user(user_id))

@posts_bp.route('/by-user/<int:user_id>', methods=['POST'])
def create_post(user_id):
    json_data = request.get_json() or {}
    try:
        dto = CreatePostDto(**json_data)
    except TypeError:
        abort(400, "Missing required fields: title, content")
    if not isinstance(dto.title, str) or not isinstance(dto.content, str):
        abort(400, "Invalid data types")
    return jsonify(service.create_post(user_id, dto)), 201

@posts_bp.route('/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    json_data = request.get_json() or {}
    dto = UpdatePostDto(**json_data)
    if not isinstance(dto.email, str) or not isinstance(dto.content, str):
        abort(400, "Invalid data types")
    result = service.update_post(post_id, dto)
    return jsonify(result)

@posts_bp.route('/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    return jsonify(service.delete_post(post_id))

@posts_bp.route('/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    data = request.get_json() or {}
    return jsonify(service.like_post(post_id, data.get('userId')))

@posts_bp.route('/<int:post_id>/like', methods=['DELETE'])
def unlike_post(post_id):
    data = request.get_json() or {}
    return jsonify(service.unlike_post(post_id, data.get('userId')))


#Comments
@posts_bp.route('/<int:post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    return jsonify(commentsService.get_post_comments(post_id))

@posts_bp.route('/<int:post_id>/comments', methods=['POST'])
def add_comment(post_id):
    json_data = request.get_json() or {}
    try:
        dto = CreateCommentDto(**json_data)
    except TypeError:
        abort(400, "Missing required fields: user_id, content")
    if not isinstance(dto.user_id, int) or not isinstance(dto.content, str):
        abort(400, "Invalid data types")
    return jsonify(commentsService.add_comment(post_id, dto)), 201

@posts_bp.route('/<int:post_id>/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(post_id, comment_id):
    return jsonify(commentsService.delete_comment(post_id, comment_id))