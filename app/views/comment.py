import json

from bson import ObjectId
from flask import jsonify, g, request
from flask_classful import FlaskView, route
from marshmallow import ValidationError

from app.models.comment import Comment
from app.models.comment_like import CommentLike, LikeStatus
from app.serializers.comment import CommentCreateSchema, CommentEditSchema, SimpleCommentSchema, CommentSchema, \
    PaginatedCommentSchema
from app.serializers.like import ChangeLikeStatusSchema
from app.utils import auth_required


class CommentView(FlaskView):
    # 댓글 목록 조회
    @auth_required
    def index(self, board_id, post_id, page=1):
        # 게시글 조회수 증가
        find_comments = Comment.objects(post=post_id, deleted=False, is_child=False).paginate(page=page, per_page=10)
        comments = PaginatedCommentSchema().dump(find_comments)

        return jsonify(comments), 200

    # 댓글 상세조회
    @auth_required
    def get(self, board_id, post_id, comment_id):
        find_comment = Comment.objects(post=post_id, deleted=False, id=comment_id).get_or_404()
        comment = CommentSchema(exclude={'post', 'writer.created_time', 'writer.last_login_time'}).dump(find_comment)

        return jsonify(comment), 200

    # 댓글 작성
    @auth_required
    def post(self, board_id, post_id):
        try:
            form = CommentCreateSchema().load(json.loads(request.data))
            form.writer = g.member_id
            form.board = ObjectId(board_id)
            form.post = ObjectId(post_id)

            form.save()
        except ValidationError as err:
            return err

        return jsonify(message='댓글이 작성되었습니다.'), 200

    # 대댓글 작성
    @route('/<comment_id>', methods=['POST'])
    @auth_required
    def child(self, board_id, post_id, comment_id):
        try:
            form = CommentCreateSchema().load(json.loads(request.data))
            form.parent_comment = ObjectId(comment_id)
            form.writer = g.member_id
            form.board = ObjectId(board_id)
            form.post = ObjectId(post_id)
            form.is_child = True

            form.save()
        except ValidationError as err:
            return err

        return jsonify(message='댓글이 작성되었습니다.'), 200

    # 댓글 수정
    @auth_required
    def put(self, board_id, post_id, comment_id):
        try:
            form = CommentEditSchema().load(json.loads(request.data))
            find_comment = Comment.objects(post_id=post_id, id=comment_id).first()

            if not find_comment.is_writer:
                return jsonify(message="본인이 작성한 댓글이 아니면 수정 할 수 없습니다."), 403

            find_comment.update_comment_modified_time()
            comment = Comment(**form)
            find_comment.update(comment)
        except ValidationError as err:
            return err

        return jsonify(message='댓글이 수정되었습니다.'), 200

    # 댓글 삭제
    @auth_required
    def delete(self, board_id, post_id, comment_id):
        try:
            find_comment = Comment.objects(post_id=post_id, id=comment_id).first()
            find_comment.soft_delete()
        except ValidationError as err:
            return err

        return jsonify(message='댓글이 삭제되었습니다.'), 200

    # 댓글 좋아요
    @route('/<comment_id>/like', methods=['POST'])
    @auth_required
    def like(self, board_id, post_id, comment_id):
        try:
            find_comment = Comment.objects(post_id=post_id, id=comment_id).first()
            member_id = str(g.member_id)

            find_comment.like(member_id)
        except ValidationError as err:
            return err

        return jsonify(message='좋아요를 눌렀습니다.'), 200

    # 댓글 좋아요
    @route('/<comment_id>/like', methods=['POST'])
    @auth_required
    def like(self, board_id, post_id, comment_id):
        find_comment = Comment.objects(post_id=post_id, id=comment_id).get_or_404()
        find_comment_like = CommentLike.objects(member=str(g.member_id), comment=comment_id).first()

        data = {"status": LikeStatus.LIKE.value}

        if not find_comment_like:
            form = ChangeLikeStatusSchema().loads(json.dumps(data))
            comment_like = CommentLike(**form)
            comment_like.member=ObjectId(g.member_id)
            comment_like.post=ObjectId(post_id)
            comment_like.save()
            find_comment.change_like_dislike_count("좋아요")
        elif find_comment_like.status == 'dislike':
            form = ChangeLikeStatusSchema().loads(json.dumps(data))
            find_comment_like.update(**form)
            find_comment.change_like_dislike_count("싫어요>좋아요")

        return jsonify(message='좋아요를 눌렀습니다.'), 200

    # 댓글 싫어요
    @route('/<comment_id>/like', methods=['POST'])
    @auth_required
    def dislike(self, board_id, post_id, comment_id):
        find_comment = Comment.objects(post_id=post_id, id=comment_id).get_or_404()
        find_comment_like = CommentLike.objects(member=str(g.member_id), comment=comment_id).first()

        data = {"status": LikeStatus.DISLIKE.value}

        if not find_comment_like:
            form = ChangeLikeStatusSchema().loads(json.dumps(data))
            comment_like = CommentLike(**form)
            comment_like.member = ObjectId(g.member_id)
            comment_like.post = ObjectId(post_id)
            comment_like.save()
            find_comment.change_like_dislike_count("싫어요")
        elif find_comment_like.status == 'like':
            form = ChangeLikeStatusSchema().loads(json.dumps(data))
            find_comment_like.update(**form)
            find_comment.change_like_dislike_count("좋아요>싫어요")

        return jsonify(message='싫어요를 눌렀습니다.'), 200

    # 댓글 좋아요,싫어요 취소
    @route('/<comment_id>/cancel', methods=['DELETE'])
    @auth_required
    def cancel(self, board_id, post_id, comment_id):
        find_comment = Comment.objects(post_id=post_id, id=comment_id).get_or_404()
        find_comment_like = CommentLike.objects(member=str(g.member_id), comment=comment_id).first()

        if find_comment_like:
            if find_comment_like.status == 'like':
                find_comment_like.delete()
                find_comment.change_like_dislike_count("좋아요취소")
            elif find_comment_like.status == 'dislike':
                find_comment_like.delete()
                find_comment.change_like_dislike_count("싫어요취소")

        return jsonify(message='취소 했습니다.'), 200
