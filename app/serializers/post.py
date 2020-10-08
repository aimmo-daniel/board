from flask import g
from marshmallow import Schema, fields, post_load

from app.models.post import Post
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
    writer = fields.Nested(MemberSchema, description='글쓴이 정보')
    tags = fields.List(fields.String(), description='태그 목록')
    like_count = fields.Int(description='좋아요수')
    dislike_count = fields.Int(description='싫어요수')
    view_count = fields.Int(description='조회수')


# 게시글 목록 조회를 위한 스키마
class SimplePostSchema(Schema):
    id = fields.String(description='게시물 PK')
    title = fields.String(description='글 제목')
    created_time = fields.DateTime(description='글 생성 시간')
    tags = fields.List(fields.String(), description='태그 목록')
    like_count = fields.Int(description='좋아요수')
    dislike_count = fields.Int(description='싫어요수')
    view_count = fields.Int(description='조회수')


# 내가쓴 글 목록 조회를 위한 스키마
class MyPostsSchema(Schema):
    id = fields.String(description='게시물 PK')
    title = fields.String(description='글 제목')
    created_time = fields.DateTime(description='글 생성 시간')
    board = fields.Nested(BoardSchema, description='게시판 정보')
    tags = fields.List(fields.String(), description='태그 목록')
    like_count = fields.Int(description='좋아요수')
    dislike_count = fields.Int(description='싫어요수')
    view_count = fields.Int(description='조회수')


# 게시물 쓰기를 위한 스키마
class PostCreateSchema(Schema):
    title = fields.String(description='글 제목')
    content = fields.String(description='글 내용')
    tags = fields.List(fields.String(), description='태그 목록')

    @post_load
    def make_post(self, data, **kwargs):
        return Post(**data)


# 게시물 수정을 위한 스키마
class PostEditSchema(Schema):
    content = fields.String(description='글 내용')
    tags = fields.List(fields.String(), description='태그 목록')


class PaginatedPostSchema(Schema):
    total = fields.Integer()
    items = fields.Nested(SimplePostSchema, many=True)