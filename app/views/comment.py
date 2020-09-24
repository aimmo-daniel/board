from flask import jsonify, request
from flask_classful import FlaskView, route

from app.service import commentService
from app.utils import auth_required


class CommentView(FlaskView):
    # 댓글 작성
    @route('', methods=['POST'])
    @auth_required
    def create(self, board_id, post_id):
        commentService.createComment(post_id, request.data)
        return jsonify(message='댓글이 작성되었습니다.'), 200

    # 댓글 수정
    @route('/<comment_id>', methods=['PUT'])
    @auth_required
    def update(self, board_id, post_id, comment_id):
        commentService.editComment(post_id, comment_id, request.data)
        return jsonify(message='댓글이 수정되었습니다.'), 200

    # 댓글 삭제
    @route('/<comment_id>', methods=['DELETE'])
    @auth_required
    def delete(self, board_id, post_id, comment_id):
        commentService.deleteComment(post_id, comment_id)
        return jsonify(message='댓글이 삭제되었습니다.'), 200

    # 댓글 좋아요
    @route('/<comment_id>/like', methods=['PUT'])
    @auth_required
    def like(self, board_id, post_id, comment_id):
        commentService.like(post_id, comment_id)
        return jsonify(message='좋아요를 눌렀습니다.'), 200

    # 댓글 좋아요 취소
    @route('/<comment_id>/unlike', methods=['PUT'])
    @auth_required
    def unlike(self, board_id, post_id, comment_id):
        commentService.unlike(post_id, comment_id)
        return jsonify(message='좋아요를 취소했습니다.'), 200
