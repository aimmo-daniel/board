import json
from collections import OrderedDict

from flask import g, current_app
from marshmallow import ValidationError

from app.models.board import Board
from app.models.post import Post, Category
from app.serializers.board import BoardSchema
from app.serializers.post import PostCreateSchema, PostSchema


# 게시판 상세정보 + 게시글 목록 조회
def board_detail(board_id):
    find_board = Board.objects(id=board_id).get()
    board_info = BoardSchema(exclude={'deleted'}).dump(find_board)

    find_post_list = Post.objects(board=board_id, deleted=False).order_by('-type') #공지사항이 위로

    post_list = PostSchema(exclude={'board', 'deleted', 'deleted_time', 'writer.deleted', 'writer.create_time', 'writer.last_login'}).dump(find_post_list, many=True)

    result = OrderedDict()
    result['board'] = board_info
    result['post_list'] = post_list

    # Json 변환시에도 OrderDict 순서 보장
    response = current_app.response_class(json.dumps(result, sort_keys=False), mimetype=current_app.config['JSONIFY_MIMETYPE'])

    return response


# 게시글 작성
def create_post(board_id, data):
    format_data = json.loads(data)
    format_data['board'] = board_id
    format_data['writer'] = str(g.member_id)

    if 'type' in format_data:
        if format_data['type'] is True:
            format_data['type'] = Category.notice.value
        else:
            format_data['type'] = Category.general.value
    else:
        format_data['type'] = Category.general.value

    try:
        result = PostCreateSchema().load(format_data)
    except ValidationError as err:
        return err

    result.save()


# 게시글 수정
def edit_post(board_id, post_id, data):
    format_data = json.loads(data)
    request_title = format_data['title']
    request_content = format_data['content']

    if 'notice' in format_data:
        if format_data['type'] is True:
            format_data['type'] = Category.notice.value
        else:
            format_data['type'] = Category.general.value
    else:
        format_data['type'] = Category.general

    find_post = Post.objects(id=post_id).get()
    find_post.edit_post(request_title, request_content)


# 게시글 삭제
def delete_post(board_id, post_id):
    find_post = Post.objects(id=post_id, board=board_id).get()
    find_post.soft_delete()


# 게시글 좋아요
def like_post(board_id, post_id):
    find_post = Post.objects(id=post_id, board=board_id).get()
    member_id = str(g.member_id)

    find_post.like(member_id)


# 게시글 좋아요 취소
def unlike_post(board_id, post_id):
    find_post = Post.objects(id=post_id, board=board_id).get()
    member_id = str(g.member_id)

    find_post.unlike(member_id)