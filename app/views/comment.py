from flask import jsonify, request
from flask_classful import FlaskView, route

from app.service import comment_service
from app.utils import auth_required


class CommentView(FlaskView):
    # 게시글 상세(+댓글 목록)
    @route('', methods=['GET'])
    @auth_required
    def post_comments(self, board_id, post_id):
        post_comments = comment_service.post_detail(board_id, post_id)
        return post_comments

    # 댓글 작성
    @route('', methods=['POST'])
    @auth_required
    def create(self, board_id, post_id):
        comment_service.create_comment(post_id, request.data)
        return jsonify(message='댓글이 작성되었습니다.'), 200

    # 댓글 수정
    @route('/<comment_id>', methods=['PUT'])
    @auth_required
    def edit(self, board_id, post_id, comment_id):
        comment_service.edit_comment(post_id, comment_id, request.data)
        return jsonify(message='댓글이 수정되었습니다.'), 200

    # 댓글 삭제
    @route('/<comment_id>', methods=['DELETE'])
    @auth_required
    def delete(self, board_id, post_id, comment_id):
        comment_service.delete_comment(post_id, comment_id)
        return jsonify(message='댓글이 삭제되었습니다.'), 200

    # 댓글 좋아요
    @route('/<comment_id>/like', methods=['PUT'])
    @auth_required
    def like(self, board_id, post_id, comment_id):
        comment_service.like_comment(post_id, comment_id)
        return jsonify(message='좋아요를 눌렀습니다.'), 200

    # 댓글 좋아요 취소
    @route('/<comment_id>/unlike', methods=['PUT'])
    @auth_required
    def unlike(self, board_id, post_id, comment_id):
        comment_service.unlike_comment(post_id, comment_id)
        return jsonify(message='좋아요를 취소했습니다.'), 200
