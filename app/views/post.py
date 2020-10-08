import json

from bson import ObjectId
from flask import request, jsonify, g
from flask_classful import FlaskView, route
from marshmallow import ValidationError

from app.models.board import Board
from app.models.post import Post
from app.models.post_like import PostLike, LikeStatus
from app.serializers.like import ChangeLikeStatusSchema
from app.serializers.post import PostCreateSchema, PostEditSchema, SimplePostSchema, PostSchema, PaginatedPostSchema
from app.utils import auth_required


class PostView(FlaskView):
    # 게시글 목록 조회
    @auth_required
    def index(self, board_id, page=1):
        board = Board.objects(id=board_id, deleted=False).get_or_404()
        find_posts = Post.objects(board=board_id, deleted=False).paginate(page=page, per_page=10)
        posts = PaginatedPostSchema().dump(find_posts)

        return jsonify(posts), 200

    # 게시글 상세정보 조회
    @auth_required
    def get(self, board_id, post_id):
        board = Board.objects(id=board_id, deleted=False).get_or_404()
        find_post = Post.objects(board=board_id, id=post_id, deleted=False).get_or_404()
        find_post.increase_view_count()

        post_detail = PostSchema().dump(find_post)

        return jsonify(post_detail), 200

    # 게시글 쓰기
    @auth_required
    def post(self, board_id):
        try:
            if not Board.objects(id=board_id, deleted=False).first():
                return jsonify(message="존재하지 않는 게시판입니다"), 404

            form = PostCreateSchema().load(json.loads(request.data))
            form.board = ObjectId(board_id)
            form.writer = ObjectId(g.member_id)

            form.save()
        except ValidationError as err:
            return jsonify(err.messages), 422

        return jsonify(message='게시글이 작성되었습니다.'), 200

    # 게시글 수정
    @auth_required
    def put(self, board_id, post_id):
        try:
            if not Board.objects(id=board_id, deleted=False).first():
                return jsonify(message="존재하지 않는 게시판입니다"), 404

            form = PostEditSchema().load(json.loads(request.data))

            find_post = Post.objects(id=post_id).first()
            find_post.update_post_modified_time()
            post = Post(**form)
            find_post.update(post)
        except ValidationError as err:
            return jsonify(err.messages), 422

        return jsonify(message='게시판 이름이 변경되었습니다.'), 200

    # 게시글 삭제
    @auth_required
    def delete(self, board_id, post_id):
        find_post = Post.objects(id=post_id, board=board_id).first()
        find_post.soft_delete()
        return jsonify(message='게시판이 삭제되었습니다.'), 200

    # 게시글 좋아요
    @route('/<post_id>/like', methods=['POST'])
    @auth_required
    def like(self, board_id, post_id):
        find_post = Post.objects(id=post_id, board=board_id).get_or_404()
        find_post_like = PostLike.objects(member=str(g.member_id), post=post_id).first()

        data = {"status": LikeStatus.LIKE.value}

        if not find_post_like:
            form = ChangeLikeStatusSchema().loads(json.dumps(data))
            post_like = PostLike(**form)
            post_like.member=ObjectId(g.member_id)
            post_like.post=ObjectId(post_id)
            post_like.save()
            find_post.change_like_dislike_count("좋아요")
        elif find_post_like.status == 'dislike':
            form = ChangeLikeStatusSchema().loads(json.dumps(data))
            find_post_like.update(**form)
            find_post.change_like_dislike_count("싫어요>좋아요")

        return jsonify(message='좋아요를 눌렀습니다.'), 200

    # 게시글 싫어요
    @route('/<post_id>/dislike', methods=['POST'])
    @auth_required
    def dislike(self, board_id, post_id):
        find_post = Post.objects(id=post_id, board=board_id).get_or_404()
        find_post_like = PostLike.objects(member=str(g.member_id), post=post_id).first()

        data = {"status": LikeStatus.DISLIKE.value}

        if not find_post_like:
            form = ChangeLikeStatusSchema().loads(json.dumps(data))
            post_like = PostLike(**form)
            post_like.member = ObjectId(g.member_id)
            post_like.post = ObjectId(post_id)
            post_like.save()
            find_post.change_like_dislike_count("싫어요")
        elif find_post_like.status == 'like':
            form = ChangeLikeStatusSchema().loads(json.dumps(data))
            find_post_like.update(**form)
            find_post.change_like_dislike_count("좋아요>싫어요")

        return jsonify(message='싫어요를 눌렀습니다.'), 200

    # 게시글 좋아요,싫어요 취소
    @route('/<post_id>/cancel', methods=['DELETE'])
    @auth_required
    def cancel(self, board_id, post_id):
        find_post = Post.objects(id=post_id, board=board_id).get_or_404()
        find_post_like = PostLike.objects(member=str(g.member_id), post=post_id).first()

        if find_post_like:
            if find_post_like.status == 'like':
                find_post_like.delete()
                find_post.change_like_dislike_count("좋아요취소")
            elif find_post_like.status == 'dislike':
                find_post_like.delete()
                find_post.change_like_dislike_count("싫어요취소")

        return jsonify(message='취소 했습니다.'), 200
