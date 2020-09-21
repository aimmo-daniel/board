from marshmallow import Schema, fields, post_load

from app.models.post import Post
from app.serializers.member import MemberSchema


class CommentSchema(Schema):
    id = fields.String(description='댓글 PK')
    content = fields.String(description='글 내용')
    create_time = fields.Date(description='글 생성 시간')
    modified_time = fields.DateTime(description='글 수정 시간')
    deleted_time = fields.DateTime(description='글 삭제 시간')
    deleted = fields.Boolean(description='글 삭제 여부')
    writer = fields.Nested(MemberSchema, dump_only=('id', 'username'))
    like_count = fields.Int(description='좋아요수')


class CommentCreateSchema(Schema):
    content = fields.String(description='댓글 내용')
    writer = fields.String(description='member_id')
    post_id = fields.String(description='post_id')

    @post_load
    def make_comment(self, data, **kwargs):
        return Post(**data)