from flask import request, jsonify
from flask_classful import FlaskView, route

from app.service import postService
from app.utils import auth_required


class PostView(FlaskView):
    # 게시글 조회(+댓글 목록)
    @route('/<post_id>', methods=['GET'])
    @auth_required
    def detail(self, board_id, post_id, page=1):
        post_detail = postService.postDetail(board_id, post_id, page)
        return post_detail

    # 게시글 쓰기
    @route('', methods=['POST'])
    @auth_required
    def create(self, board_id):
        postService.writePost(board_id, request.data)
        return jsonify(message='게시글이 작성되었습니다.'), 200

    # 게시글 수정
    @route('/<post_id>', methods=['PUT'])
    @auth_required
    def edit(self, board_id, post_id):
        postService.editPost(board_id, post_id, request.data)
        return jsonify(message='게시판 이름이 변경되었습니다.'), 200

    # 게시글 삭제
    @route('/<post_id>', methods=['DELETE'])
    @auth_required
    def delete(self, board_id, post_id):
        postService.deletePost(board_id, post_id)
        return jsonify(message='게시판이 삭제되었습니다.'), 200

    # 게시글 좋아요
    @route('/<post_id>/like', methods=['PUT'])
    @auth_required
    def like(self, board_id, post_id):
        postService.like(board_id, post_id)
        return jsonify(message='좋아요를 눌렀습니다.'), 200

    # 게시글 좋아요 취소
    @route('/<post_id>/unlike', methods=['PUT'])
    @auth_required
    def unlike(self, board_id, post_id):
        postService.unlike(board_id, post_id)
        return jsonify(message='좋아요를 취소했습니다.'), 200
