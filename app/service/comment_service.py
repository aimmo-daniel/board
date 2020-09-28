import json
from collections import OrderedDict

from flask import g, current_app
from marshmallow import ValidationError

from app.models.comment import Comment
from app.models.post import Post
from app.serializers.comment import CommentCreateSchema, CommentSchema
from app.serializers.post import PostSchema


# 게시글 상세 조회 + 댓글 목록 조회
def post_detail(board_id, post_id):
    find_post = Post.objects(id=post_id, board=board_id).get()
    find_post.increase_view_count()
    post_info = PostSchema(exclude={'deleted', 'deleted_time', 'board.deleted', 'board.create_time', 'writer.deleted', 'writer.deleted_time', 'writer.last_login', 'writer.create_time'}).dump(find_post)

    find_comment_list = Comment.objects(post=post_id, deleted=False).order_by('+create_time', '-like_count')
    comment_list = CommentSchema(exclude={'deleted_time', 'post', 'deleted', 'writer.create_time', 'writer.deleted', 'writer.last_login', 'writer.deleted_time'}).dump(find_comment_list, many=True)

    result = OrderedDict()
    result['post'] = post_info
    result['comment_list'] = comment_list

    # Json 변환시에도 OrderDict 순서 보장
    response = current_app.response_class(json.dumps(result, sort_keys=False), mimetype=current_app.config['JSONIFY_MIMETYPE'])
    return response


# 댓글 작성
def create_comment(post_id, data):
    format_data = json.loads(data)
    format_data['post'] = post_id
    format_data['writer'] = str(g.member_id)

    try:
        result = CommentCreateSchema().load(format_data)
    except ValidationError as err:
        return err

    result.save()


# 댓글 수정
def edit_comment(post_id, comment_id, data):
    content = json.loads(data)['content']
    find_comment = Comment.objects(post_id=post_id, id=comment_id).get()
    find_comment.edit_comment(content)


# 댓글 삭제
def delete_comment(post_id, comment_id):
    find_comment = Comment.objects(post_id=post_id, id=comment_id).get()
    find_comment.soft_delete()


# 댓글 좋아요
def like_comment(post_id, comment_id):
    find_comment = Comment.objects(post_id=post_id, id=comment_id).get()
    member_id = str(g.member_id)

    find_comment.like(member_id)


# 댓글 좋아요 취소
def unlike_comment(post_id, comment_id):
    find_comment = Comment.objects(post_id=post_id, id=comment_id).get()
    member_id = str(g.member_id)

    find_comment.unlike(member_id)