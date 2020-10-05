import json
from collections import OrderedDict

from flask import jsonify, current_app, g
from flask_apispec import use_kwargs
from flask_classful import FlaskView, route
from marshmallow import ValidationError

from app.models.comment import Comment
from app.models.post import Post
from app.serializers.comment import CommentSchema, CommentCreateSchema, CommentEditSchema
from app.serializers.post import PostSchema
from app.utils import auth_required


class CommentView(FlaskView):
    # 게시글 상세(+댓글 목록)
    @route('', methods=['GET'])
    @auth_required
    def post_comments(self, board_id, post_id):
        find_post = Post.objects(id=post_id, board=board_id).first()
        find_post.increase_view_count()

        post_info = PostSchema(exclude={'board.create_time', 'writer.last_login', 'writer.create_time'}).dump(find_post)

        find_comment_list = Comment.objects(post=post_id, deleted=False).order_by('+create_time', '-like_count')
        comment_list = CommentSchema(exclude={'post', 'writer.create_time', 'writer.last_login'}).dump(find_comment_list, many=True)

        result = OrderedDict()
        result['post'] = post_info
        result['comment_list'] = comment_list

        # Json 변환시에도 OrderDict 순서 보장
        response = current_app.response_class(json.dumps(result, sort_keys=False), mimetype=current_app.config['JSONIFY_MIMETYPE'])
        return response

    # 댓글 작성
    @route('', methods=['POST'])
    @use_kwargs(CommentCreateSchema(), locations=('json',))
    @auth_required
    def create(self, board_id, post_id, **kwargs):
        comment = Comment(post=post_id, writer=g.member_id, content=kwargs.get('name'))

        try:
            result = CommentCreateSchema().load(comment)
            result.save()
        except ValidationError as err:
            return err

        return jsonify(message='댓글이 작성되었습니다.'), 200

    # 댓글 수정
    @route('/<comment_id>', methods=['PUT'])
    @use_kwargs(CommentEditSchema(), locations=('json',))
    @auth_required
    def edit(self, board_id, post_id, comment_id, **kwargs):
        content = kwargs.get('content')
        find_comment = Comment.objects(post_id=post_id, id=comment_id).first()

        if not find_comment.is_writer:
            return jsonify(message="본인이 작성한 댓글이 아니면 수정 할 수 없습니다."), 403

        try:
            find_comment.edit_comment(content)
        except ValidationError as err:
            return err

        return jsonify(message='댓글이 수정되었습니다.'), 200

    # 댓글 삭제
    @route('/<comment_id>', methods=['DELETE'])
    @auth_required
    def delete(self, board_id, post_id, comment_id):
        try:
            find_comment = Comment.objects(post_id=post_id, id=comment_id).first()
            find_comment.soft_delete()
        except ValidationError as err:
            return err

        return jsonify(message='댓글이 삭제되었습니다.'), 200

    # 댓글 좋아요
    @route('/<comment_id>/like', methods=['PUT'])
    @auth_required
    def like(self, board_id, post_id, comment_id):
        try:
            find_comment = Comment.objects(post_id=post_id, id=comment_id).first()
            member_id = str(g.member_id)

            find_comment.like(member_id)
        except ValidationError as err:
            return err

        return jsonify(message='좋아요를 눌렀습니다.'), 200

    # 댓글 좋아요 취소
    @route('/<comment_id>/unlike', methods=['PUT'])
    @auth_required
    def unlike(self, board_id, post_id, comment_id):
        try:
            find_comment = Comment.objects(post_id=post_id, id=comment_id).first()
            member_id = str(g.member_id)

            find_comment.unlike(member_id)
        except ValidationError as err:
            return err

        return jsonify(message='좋아요를 취소했습니다.'), 200
