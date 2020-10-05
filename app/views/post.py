import json
from collections import OrderedDict

from flask import request, jsonify, current_app, g
from flask_classful import FlaskView, route
from marshmallow import ValidationError

from app.models.board import Board
from app.models.post import Post, Category
from app.serializers.board import BoardSchema
from app.serializers.post import PostSchema, PostCreateSchema, PostEditSchema
from app.service import post_service
from app.utils import auth_required


class PostView(FlaskView):
    # 게시판 상세 조회 (+게시글 목록)
    @auth_required
    def index(self, board_id):
        find_board = Board.objects(id=board_id).first()
        board = BoardSchema(exclude={'deleted'}).dump(find_board)

        find_posts = Post.objects(board=board_id, deleted=False).order_by('-type')  # 공지사항이 위로

        posts = PostSchema(exclude={'board', 'deleted', 'deleted_time', 'writer.deleted', 'writer.created_time', 'writer.last_login_time'}).dump(find_posts, many=True)

        result = OrderedDict()
        result['board'] = board
        result['posts'] = posts

        # Json 변환시에도 OrderDict 순서 보장
        response = current_app.response_class(json.dumps(result, sort_keys=False), mimetype=current_app.config['JSONIFY_MIMETYPE'])

        return response

    # 게시글 쓰기
    @auth_required
    def post(self, board_id):
        form = PostCreateSchema().load(json.loads(request.data))
        form['board'] = board_id
        form['writer'] = str(g.member_id)

        if 'type' in form:
            if form['type'] is True:
                form['type'] = Category.notice.value
            else:
                form['type'] = Category.general.value
        else:
            form['type'] = Category.general.value

        try:
            form.save()
        except ValidationError as err:
            return err

        return jsonify(message='게시글이 작성되었습니다.'), 200

    # 게시글 수정
    @auth_required
    def put(self, board_id, post_id):
        form = PostEditSchema().load(json.loads(request.data))

        if 'notice' in form:
            if form['type'] is True:
                form['type'] = Category.notice.value
            else:
                form['type'] = Category.general.value
        else:
            form['type'] = Category.general

        find_post = Post.objects(id=post_id).get()
        find_post.update_post_modified_time()
        post = Post(**form)
        find_post.update(post)

        return jsonify(message='게시판 이름이 변경되었습니다.'), 200

    # 게시글 삭제
    @auth_required
    def delete(self, board_id, post_id):
        find_post = Post.objects(id=post_id, board=board_id).get()
        find_post.soft_delete()
        return jsonify(message='게시판이 삭제되었습니다.'), 200

    # 게시글 좋아요
    @route('/<post_id>/like', methods=['POST'])
    @auth_required
    def like(self, board_id, post_id):
        find_post = Post.objects(id=post_id, board=board_id).get()
        member_id = str(g.member_id)

        find_post.like(member_id)

        return jsonify(message='좋아요를 눌렀습니다.'), 200

    # 게시글 좋아요 취소
    @route('/<post_id>/unlike', methods=['POST'])
    @auth_required
    def unlike(self, board_id, post_id):
        find_post = Post.objects(id=post_id, board=board_id).get()
        member_id = str(g.member_id)

        find_post.unlike(member_id)
        return jsonify(message='좋아요를 취소했습니다.'), 200
