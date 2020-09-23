import json
from collections import OrderedDict

from flask import g, current_app

from app.models.comment import Comment
from app.models.post import Post
from app.serializers.comment import CommentCreateSchema, CommentSchema
from app.serializers.post import PostSchema


def createComment(post_id, data):
    # 댓글 작성
    format_data = json.loads(data)
    format_data['post'] = post_id
    format_data['writer'] = str(g.member_id)

    result = CommentCreateSchema().load(format_data)
    result.save()


def editComment(post_id, comment_id, data):
    # 댓글 수정
    content = json.loads(data)['content']
    find_comment = Comment.objects(post_id=post_id, id=comment_id).get()
    find_comment.edit_comment(content)


def deleteComment(post_id, comment_id):
    # 댓글 삭제
    find_comment = Comment.objects(post_id=post_id, id=comment_id).get()
    find_comment.soft_delete()


def like(post_id, comment_id):
    # 댓글 좋아요
    find_comment = Comment.objects(post_id=post_id, id=comment_id).get()
    member_id = str(g.member_id)

    find_comment.like(member_id)


def unlike(post_id, comment_id):
    # 댓글 좋아요 취소
    find_comment = Comment.objects(post_id=post_id, id=comment_id).get()
    member_id = str(g.member_id)

    find_comment.unlike(member_id)