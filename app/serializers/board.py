from marshmallow import Schema, fields, post_load

from app.models.board import Board


# 게시판 조회 스키마
class BoardSchema(Schema):
    id = fields.String(description='게시판 PK')
    name = fields.String(description='게시판명')
    created_time = fields.DateTime(description='게시판 생성일')


# 게시판 생성 스키마
class BoardCreateSchema(Schema):
    name = fields.String(description='게시판명')

    @post_load
    def make_board(self, data, **kwargs):
        return Board(**data)


# 게시판 수정 스키마
class BoardEditNameSchema(Schema):
    name = fields.String(description='게시판명')