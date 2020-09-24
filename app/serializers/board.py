from marshmallow import Schema, fields, post_load

from app.models.board import Board


class BoardSchema(Schema):
    id = fields.String(description='게시판 PK')
    name = fields.String(description='게시판명')
    create_time = fields.DateTime(description='게시판 생성일')
    deleted = fields.Boolean(description='삭제 여부')

    @post_load
    def makeBoard(self, data, **kwargs):
        return Board(**data)