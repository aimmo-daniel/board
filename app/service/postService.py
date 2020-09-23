import json
from collections import OrderedDict

from flask import g, current_app

from app.models.comment import Comment
from app.models.post import Post
from app.serializers.comment import CommentSchema
from app.serializers.post import PostCreateSchema, PostSchema


def postDetail(board_id, post_id, page):
    # 게시글 조회 + 댓글 목록 조회
    find_post = Post.objects(id=post_id, board=board_id).get()
    post_info = PostSchema(exclude={'board.deleted', 'board.create_time', 'writer.deleted', 'writer.last_login', 'writer.create_time'}).dump(find_post)

    find_comment_list = Comment.objects(post=post_id, deleted=False).order_by('+create_time', '-like_count')
    comment_list = CommentSchema(exclude={'post', 'deleted', 'writer.create_time', 'writer.deleted', 'writer.last_login'}).dump(find_comment_list, many=True)

    result = OrderedDict()
    result['post'] = post_info
    result['comment_list'] = comment_list

    # Json 변환시에도 OrderDict 순서 보장
    response = current_app.response_class(json.dumps(result, sort_keys=False), mimetype=current_app.config['JSONIFY_MIMETYPE'])
    return response


def writePost(board_id, data):
    # 게시글 작성
    format_data = json.loads(data)
    format_data['board'] = board_id
    format_data['writer'] = str(g.member_id)

    result = PostCreateSchema().load(format_data)
    result.save()


def editPost(board_id, post_id, data):
    # 게시글 수정
    format_data = json.loads(data)
    request_title = format_data['title']
    request_content = format_data['content']

    find_post = Post.objects(id=post_id).get()
    find_post.edit_post(request_title, request_content)


def deletePost(board_id, post_id):
    # 게시글 삭제
    find_post = Post.objects(id=post_id, board=board_id).get()
    find_post.soft_delete()


def like(board_id, post_id):
    # 게시글 좋아요
    find_post = Post.objects(id=post_id, board=board_id).get()
    member_id = str(g.member_id)

    find_post.like(member_id)


def unlike(board_id, post_id):
    # 게시글 좋아요 취소
    find_post = Post.objects(id=post_id, board=board_id).get()
    member_id = str(g.member_id)

    find_post.unlike(member_id)