from flask import request, jsonify
from flask_classful import FlaskView, route

from app.service import post_service
from app.utils import auth_required


class PostView(FlaskView):
    # 게시판 상세 조회 (+게시글 목록)
    @auth_required
    def index(self, board_id):
        board_posts = post_service.board_detail(board_id)
        return board_posts

    # 게시글 쓰기
    @auth_required
    def post(self, board_id):
        post_service.create_post(board_id, request.data)
        return jsonify(message='게시글이 작성되었습니다.'), 200

    # 게시글 수정
    @auth_required
    def put(self, board_id, post_id):
        post_service.edit_post(board_id, post_id, request.data)
        return jsonify(message='게시판 이름이 변경되었습니다.'), 200

    # 게시글 삭제
    @auth_required
    def delete(self, board_id, post_id):
        post_service.delete_post(board_id, post_id)
        return jsonify(message='게시판이 삭제되었습니다.'), 200

    # 게시글 좋아요
    @route('/<post_id>/like', methods=['POST'])
    @auth_required
    def like(self, board_id, post_id):
        post_service.like_post(board_id, post_id)
        return jsonify(message='좋아요를 눌렀습니다.'), 200

    # 게시글 좋아요 취소
    @route('/<post_id>/unlike', methods=['POST'])
    @auth_required
    def unlike(self, board_id, post_id):
        post_service.unlike_post(board_id, post_id)
        return jsonify(message='좋아요를 취소했습니다.'), 200
