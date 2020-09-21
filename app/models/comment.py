from datetime import datetime

from mongoengine import Document, StringField, DateTimeField, BooleanField, ReferenceField, IntField

from app.models.member import Member


class Comment(Document):
    content = StringField(required=True, description='댓글 내용')
    create_time = DateTimeField(default=datetime.utcnow().strftime('%B %d %Y - %H:%M:%S'), description='댓글 생성 시간')
    modified_time = DateTimeField(description='댓글 수정 시간')
    deleted_time = DateTimeField(description='댓글 삭제 시간')
    deleted = BooleanField(default=False, description='글 삭제 여부')
    writer = ReferenceField(Member, required=True, description='글쓴이(Member_id)')
    like_count = IntField(required=True, default=0, min_value=0, description='좋아요수')

    """좋아요"""
    def like(self):
        self.likes += 1

    """좋아요 취소"""
    def unlike(self):
        if self.likes > 0:
            self.likes -= 1

    """댓글 삭제"""
    def soft_delete(self):
        self.deleted = not self.deleted