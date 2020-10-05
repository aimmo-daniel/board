from flask import g
from marshmallow import Schema, fields, post_load

from app.models.post import Post, Category
from app.serializers.board import BoardSchema
from app.serializers.member import MemberSchema


# 게시글 조회를 위한 스키마
class PostSchema(Schema):
    id = fields.String(description='게시물 PK')
    title = fields.String(description='글 제목')
    content = fields.String(description='글 내용')
    created_time = fields.DateTime(description='글 생성 시간')
    modified_time = fields.DateTime(description='글 수정 시간')
    deleted_time = fields.DateTime(description='글 삭제 시간')
    deleted = fields.Boolean(description='글 삭제 여부')
    board = fields.Nested(BoardSchema, description='게시판 정보')
    writer = fields.Nested(MemberSchema, description='글쓴이 정보')
    tags = fields.List(fields.String(), description='태그 목록')
    is_notice = fields.Method('check_post_type', description='공지사항=1, 일반게시물=0')
    my_like = fields.Method('is_clicked', description='나의 좋아요 상태')
    like_count = fields.Method('total_like_count', description='좋아요수')
    view_count = fields.Int(description='조회수')

    # 좋아요 중복 체크 확인
    def is_clicked(self, obj):
        if str(g.member_id) in obj.likes:
            return True
        else:
            return False

    # 좋아요 갯수 집계    
    def total_like_count(self, obj):
        return len(obj.likes)

    def check_post_type(self, obj):
        return obj.type


# 게시물 쓰기를 위한 스키마
class PostCreateSchema(Schema):
    board = fields.String(description='board_id')
    title = fields.String(description='글 제목')
    content = fields.String(description='글 내용')
    type = fields.Int(description='타입')
    tag_list = fields.List(fields.String(), description='태그 목록')
    writer = fields.String(description='member_id')

    @post_load
    def make_post(self, data, **kwargs):
        return Post(**data)


# 게시물 수정을 위한 스키마
class PostEditSchema(Schema):
    content = fields.String(description='글 내용')
    type = fields.Int(description='타입')
    tag_list = fields.List(fields.String(), description='태그 목록')