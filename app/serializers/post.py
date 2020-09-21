from marshmallow import Schema, fields, post_load

from app.models.post import Post
from app.serializers.member import MemberSchema


class PostSchema(Schema):
    id = fields.String(description='게시물 PK')
    title = fields.String(description='글 제목')
    content = fields.String(description='글 내용')
    create_time = fields.Date(description='글 생성 시간')
    modified_time = fields.DateTime(description='글 수정 시간')
    deleted_time = fields.DateTime(description='글 삭제 시간')
    deleted = fields.Boolean(description='글 삭제 여부')
    writer = fields.Nested(MemberSchema, dump_only=('id', 'username'))
    #tag_list = fields.List(fields.String(), description='태그 목록')
    #comment_list = fields.List(fields.Nested(CommentSchema), description='댓글 목록')
    like_count = fields.Int(description='좋아요수')
    view_count = fields.Int(description='조회수')


class PostCreateSchema(Schema):
    title = fields.String(description='글 제목')
    content = fields.String(description='글 내용')
    tag_list = fields.List(fields.String(), description='태그 목록')
    writer = fields.String(description='member_id')
    board_id = fields.String(description='board_id')

    @post_load
    def make_post(self, data, **kwargs):
        return Post(**data)