from enum import Enum

from flask_mongoengine import Document
from mongoengine import StringField, ReferenceField

from app.models.member import Member
from app.models.post import Post


class LikeStatus(Enum):
    NOACTION = "no_action"
    LIKE = "like"
    DISLIKE = "dislike"


class PostLike(Document):
    member = ReferenceField(Member, required=True, description='글쓴이(member_id)')
    post = ReferenceField(Post, required=True, description='게시물 아이디')
    status = StringField(description='좋아요 상태')