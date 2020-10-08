from marshmallow import Schema, fields, post_load

from app.models.comment import Comment
from app.models.member import Member
from app.serializers.member import MemberSchema, SimpleMemberSchema
from app.serializers.post import PostSchema


# 댓글 상세조회를 위한 스키마
class CommentSchema(Schema):
    id = fields.String(description='댓글 PK')
    content = fields.String(description='댓글 내용')
    created_time = fields.DateTime(description='댓글 생성 시간')
    like_count = fields.Int(description='좋아요수')
    dislike_count = fields.Int(description='싫어요수')
    modified_time = fields.DateTime(description='댓글 수정 시간')
    post = fields.Nested(PostSchema, description='게시글 정보')
    writer = fields.Nested(MemberSchema, description='댓글 쓴 유저 정보')
    child_comments= fields.Method('get_child_comments', description='대댓글')

    #대댓글
    def get_child_comments(self, obj):
        return SimpleCommentSchema(many=True).dump(Comment.objects(parent_comment=obj.id, deleted=False))


# 댓글 목록조회를 위한 스키마
class SimpleCommentSchema(Schema):
    id = fields.String(description='댓글 PK')
    content = fields.String(description='댓글 내용')
    created_time = fields.DateTime(description='댓글 생성 시간')
    like_count = fields.Int(description='좋아요수')
    dislike_count = fields.Int(description='싫어요수')
    writer = fields.Nested(SimpleMemberSchema, description='댓글 쓴 유저 정보')


# 댓글 생성을 위한 스키마
class CommentCreateSchema(Schema):
    post = fields.String(description='post_id')
    writer = fields.String(description='member_id')
    content = fields.String(description='댓글 내용')

    @post_load
    def make_comment(self, data, **kwargs):
        return Comment(**data)


# 댓글 수정을 위한 스키마
class CommentEditSchema(Schema):
    content = fields.String(description='댓글 내용')


# 댓글 페이징 처리를 위한 스키마
class PaginatedCommentSchema(Schema):
    total = fields.Integer()
    items = fields.Nested(SimpleCommentSchema, many=True)