from flask import jsonify, request
from flask_classful import FlaskView, route

from app.service import commentService


class CommentView(FlaskView):
    @route('', methods=['POST'])
    def create(self, post_id):
        commentService.createComment(post_id, request.data)
        return jsonify(message='댓글이 작성되었습니다.'), 200