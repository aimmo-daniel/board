from marshmallow import Schema, fields, post_load

from app.models.board import Board
from app.serializers.post import PostSchema


class BoardSchema(Schema):
    id = fields.String(description='게시판 PK')
    name = fields.String(description='게시판명')
    create_time = fields.DateTime(description='게시판 생성일')
    deleted = fields.Boolean(description='삭제 여부')

    @post_load
    def make_board(self, data, **kwargs):
        return Board(**data)


class BoardDetailSchema(Schema):
    id = fields.String(description='게시판 PK')
    name = fields.String(description='게시판명')
    create_time = fields.DateTime(description='게시판 생성일')
    deleted = fields.Boolean(description='삭제 여부')
    post_list = fields.List(fields.Nested(PostSchema, dump_only=("id", "title")), description='게시물 목록')