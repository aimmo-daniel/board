from marshmallow import Schema, fields, post_load

from app.models.post_like import PostLike
from app.serializers.member import MemberSchema
from app.serializers.post import PostSchema


class PostLikeSchema(Schema):
    id = fields.String(description='PK')
    post = fields.Nested(PostSchema, description='게시물 정보')
    member = fields.Nested(MemberSchema, description='좋아요, 싫어요 누른사람')
    status = fields.String(description='상태')
    
    
class CommentLikeSchema(Schema):
    id = fields.String(description='PK')
    comment = fields.Nested(PostSchema, description='댓글 정보')
    member = fields.Nested(MemberSchema, description='좋아요, 싫어요 누른사람')
    status = fields.String(description='상태')
    
    
class ChangeLikeStatusSchema(Schema):
    status = fields.String(description='상태')
