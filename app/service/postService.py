import json
from collections import OrderedDict

from flask import g, current_app
from marshmallow import ValidationError

from app.models.comment import Comment
from app.models.post import Post, Category
from app.serializers.comment import CommentSchema
from app.serializers.post import PostCreateSchema, PostSchema


# 게시글 조회 + 댓글 목록 조회
def postDetail(board_id, post_id, page):
    find_post = Post.objects(id=post_id, board=board_id).get()
    find_post.increaseViewCount()
    post_info = PostSchema(exclude={'board.deleted', 'board.create_time', 'writer.deleted', 'writer.last_login', 'writer.create_time'}).dump(find_post)

    find_comment_list = Comment.objects(post=post_id, deleted=False).order_by('+create_time', '-like_count')
    comment_list = CommentSchema(exclude={'post', 'deleted', 'writer.create_time', 'writer.deleted', 'writer.last_login'}).dump(find_comment_list, many=True)

    result = OrderedDict()
    result['post'] = post_info
    result['comment_list'] = comment_list

    # Json 변환시에도 OrderDict 순서 보장
    response = current_app.response_class(json.dumps(result, sort_keys=False), mimetype=current_app.config['JSONIFY_MIMETYPE'])
    return response


# 게시글 작성
def writePost(board_id, data):
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
def editPost(board_id, post_id, data):
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
    find_post.editPost(request_title, request_content)


# 게시글 삭제
def deletePost(board_id, post_id):
    find_post = Post.objects(id=post_id, board=board_id).get()
    find_post.softDelete()


# 게시글 좋아요
def like(board_id, post_id):
    find_post = Post.objects(id=post_id, board=board_id).get()
    member_id = str(g.member_id)

    find_post.like(member_id)


# 게시글 좋아요 취소
def unlike(board_id, post_id):
    find_post = Post.objects(id=post_id, board=board_id).get()
    member_id = str(g.member_id)

    find_post.unlike(member_id)