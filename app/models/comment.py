from datetime import datetime

from flask_mongoengine import Document
from mongoengine import StringField, DateTimeField, BooleanField, ReferenceField, IntField

from app.models.member import Member
from app.models.post import Post


#댓글 목록 조회
class Comment(Document):
    post = ReferenceField(Post, required=True, description='게시글 정보(post_id')
    writer = ReferenceField(Member, required=True, description='글쓴이(member_id)')
    content = StringField(required=True, description='댓글 내용')
    created_time = DateTimeField(default=datetime.utcnow().strftime('%B %d %Y - %H:%M:%S'), description='댓글 생성 시간')
    like_count = IntField(default=0, min_value=0, description='좋아요수')
    dislike_count = IntField(default=0, min_value=0, description='싫어요수')
    modified_time = DateTimeField(null=True, default=None, description='댓글 수정 시간')
    deleted = BooleanField(default=False, description='댓글 삭제 여부')
    deleted_time = DateTimeField(null=True, default=None, description='댓글 삭제 시간')
    parent_comment = ReferenceField('self', description='상위 댓글')
    is_child = BooleanField(required=True, default=False)

    # 작성자가 일치하는지 확인
    def is_writer(self, member_id):
        return self.writer.id == member_id

    def change_like_dislike_count(self, discribe):
        if discribe == "좋아요":
            self.like_count += 1
        elif discribe == "좋아요취소":
            self.like_count -= 1
        elif discribe == '싫어요':
            self.dislike_count += 1
        elif discribe == '싫어요취소':
            self.dislike_count -= 1
        elif discribe == "좋아요>싫어요":
            self.like_count -= 1
            self.dislike_count += 1
        elif discribe == "싫어요>좋아요":
            self.dislike_count -= 1
            self.like_count += 1

        self.save()

    # 댓글 수정시간 업데이트
    def update_comment_modified_time(self, content):
        self.modified_time = datetime.utcnow().strftime('%B %d %Y - %H:%M:%S')
        self.save()

    # 댓글 삭제
    def soft_delete(self):
        self.deleted = True
        self.deleted_time = datetime.utcnow().strftime('%B %d %Y - %H:%M:%S')
        self.save()