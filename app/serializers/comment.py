from flask import g
from marshmallow import Schema, fields, post_load

from app.models.comment import Comment
from app.serializers.member import MemberSchema
from app.serializers.post import PostSchema


# 댓글 조회를 위한 스키마
class CommentSchema(Schema):
    id = fields.String(description='댓글 PK')
    content = fields.String(description='댓글 내용')
    create_time = fields.DateTime(description='댓글 생성 시간')
    my_like = fields.Method('isClicked', description='나의 좋아요 상태')
    like_count = fields.Method('countLikes', description='좋아요수')
    modified_time = fields.DateTime(description='댓글 수정 시간')
    deleted = fields.Boolean(description='댓글 삭제 여부')
    deleted_time = fields.DateTime(description='댓글 삭제 시간')
    post = fields.Nested(PostSchema, description='게시글 정보')
    writer = fields.Nested(MemberSchema, description='댓글 쓴 유저 정보')

    # 좋아요 중복 체크 확인
    def isClicked(self, obj):
        if str(g.member_id) in obj.likes:
            return True
        else:
            return False

    # 댓글 좋아요수 집계
    def countLikes(self, obj):
        return len(obj.likes)


# 댓글 생성을 위한 스키마
class CommentCreateSchema(Schema):
    post = fields.String(description='post_id')
    writer = fields.String(description='member_id')
    content = fields.String(description='댓글 내용')

    @post_load
    def makeComment(self, data, **kwargs):
        return Comment(**data)