from flask import g
from marshmallow import Schema, fields, post_load

from app.models.comment import Comment
from app.serializers.member import MemberSchema
from app.serializers.post import PostSchema


class CommentSchema(Schema):
    id = fields.String(description='댓글 PK')
    content = fields.String(description='댓글 내용')
    create_time = fields.Date(description='댓글 생성 시간')
    my_like = fields.Method('is_clicked', description='나의 좋아요 상태')
    like_count = fields.Method('count_likes', description='좋아요수')
    modified_time = fields.DateTime(description='댓글 수정 시간')
    deleted = fields.Boolean(description='댓글 삭제 여부')
    deleted_time = fields.DateTime(description='댓글 삭제 시간')
    post = fields.Nested(PostSchema, description='게시글 정보')
    writer = fields.Nested(MemberSchema, description='댓글 쓴 유저 정보')

    def is_clicked(self, obj):
        if str(g.member_id) in obj.likes:
            return True
        else:
            return False

    def count_likes(self, obj):
        return len(obj.likes)


class CommentCreateSchema(Schema):
    post = fields.String(description='post_id')
    writer = fields.String(description='member_id')
    content = fields.String(description='댓글 내용')

    @post_load
    def make_comment(self, data, **kwargs):
        return Comment(**data)