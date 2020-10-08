from enum import Enum

from flask_mongoengine import Document
from mongoengine import StringField, ReferenceField

from app.models.comment import Comment
from app.models.member import Member


class LikeStatus(Enum):
    NOACTION = "no_action"
    LIKE = "like"
    HATE = "hate"


class CommentLike(Document):
    member = ReferenceField(Member, required=True, description='글쓴이(member_id)')
    comment = ReferenceField(Comment, required=True, description='댓글(comment_id)')
    status = StringField(description='좋아요 상태')