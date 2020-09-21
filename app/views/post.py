from flask import request, jsonify
from flask_classful import FlaskView, route

from app.service import postService


class PostView(FlaskView):
    @route('/<post_id>', methods=['GET'])
    def detail(self, post_id, page=1):
        post_detail = postService.postDetail(post_id, page)
        return jsonify(post_detail), 200

    @route('', methods=['POST'])
    def create(self, board_id):
        postService.writePost(board_id, request.data)
        return jsonify(message='게시글이 작성되었습니다.'), 200

    @route('/<post_id>', methods=['PUT'])
    def edit(self, post_id):
        postService.editPost(post_id, request.data)
        return jsonify(message='게시판 이름이 변경되었습니다.'), 200

    @route('/<post_id>', methods=['DELETE'])
    def delete(self, post_id):
        postService.deletePost(post_id)
        return jsonify(message='게시판이 삭제되었습니다.'), 200