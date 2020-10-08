from unittest import result

from flask import jsonify, g
from flask_classful import FlaskView, route
from marshmallow import ValidationError

from app.models.comment import Comment
from app.models.post import Post
from app.serializers.post import MyPostsSchema
from app.utils import auth_required


class MyPageView(FlaskView):

    @route('/written/posts', methods=['GET'])
    @auth_required
    def my_written_posts(self):
        try:
            find_posts = Post.objects(writer=g.member_id, deleted=False, many=True)
            my_posts = MyPostsSchema().dump(find_posts, many=True)
        except ValidationError as err:
            return err

        return jsonify(my_posts), 200

    @route('/written/comments', methods=['GET'])
    @auth_required
    def my_written_comments(self):
        try:
            find_comments = Comment.objects(writer=g.member_id, deleted=False).order_by()
            #my_comments = MyCommentsSchema().dump(find_comments, many=True)
        except ValidationError as err:
            return err

        return jsonify(result), 200

    @route('/like/posts', methods=['GET'])
    @auth_required
    def my_like_posts(self):
        try:
            pass
        except ValidationError as err:
            return err

        return jsonify(result), 200

    @route('/like/comments', methods=['GET'])
    @auth_required
    def my_like_comments(self):
        try:
            pass
        except ValidationError as err:
            return err

        return jsonify(result), 200


