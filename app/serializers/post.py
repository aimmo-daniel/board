from flask import g
from marshmallow import Schema, fields, post_load

from app.models.post import Post
from app.serializers.board import BoardSchema
from app.serializers.member import MemberSchema


class PostSchema(Schema):
    id = fields.String(description='게시물 PK')
    title = fields.String(description='글 제목')
    content = fields.String(description='글 내용')
    create_time = fields.Date(description='글 생성 시간')
    modified_time = fields.DateTime(description='글 수정 시간')
    deleted_time = fields.DateTime(description='글 삭제 시간')
    deleted = fields.Boolean(description='글 삭제 여부')
    board = fields.Nested(BoardSchema, description='게시판 정보')
    writer = fields.Nested(MemberSchema, description='글쓴이 정보')
    tag_list = fields.List(fields.String(), description='태그 목록')
    my_like = fields.Method('is_clicked', description='나의 좋아요 상태')
    like_count = fields.Method('count_likes', description='좋아요수')
    view_count = fields.Int(description='조회수')

    def is_clicked(self, obj):
        if str(g.member_id) in obj.likes:
            return True
        else:
            return False

    def count_likes(self, obj):
        return len(obj.likes)


class PostCreateSchema(Schema):
    board = fields.String(description='board_id')
    title = fields.String(description='글 제목')
    content = fields.String(description='글 내용')
    tag_list = fields.List(fields.String(), description='태그 목록')
    writer = fields.String(description='member_id')

    @post_load
    def make_post(self, data, **kwargs):
        return Post(**data)