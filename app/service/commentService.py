import json

from flask import g
from marshmallow import ValidationError

from app.models.comment import Comment
from app.serializers.comment import CommentCreateSchema


# 댓글 작성
def createComment(post_id, data):
    format_data = json.loads(data)
    format_data['post'] = post_id
    format_data['writer'] = str(g.member_id)

    try:
        result = CommentCreateSchema().load(format_data)
    except ValidationError as err:
        return err

    result.save()


# 댓글 수정
def editComment(post_id, comment_id, data):
    content = json.loads(data)['content']
    find_comment = Comment.objects(post_id=post_id, id=comment_id).get()
    find_comment.editComment(content)


# 댓글 삭제
def deleteComment(post_id, comment_id):
    find_comment = Comment.objects(post_id=post_id, id=comment_id).get()
    find_comment.softDelete()


# 댓글 좋아요
def like(post_id, comment_id):
    find_comment = Comment.objects(post_id=post_id, id=comment_id).get()
    member_id = str(g.member_id)

    find_comment.like(member_id)


# 댓글 좋아요 취소
def unlike(post_id, comment_id):
    find_comment = Comment.objects(post_id=post_id, id=comment_id).get()
    member_id = str(g.member_id)

    find_comment.unlike(member_id)