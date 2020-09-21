import json

from app.serializers.post import PostCreateSchema


def postDetail(post_id, page):
    return None


def writePost(board_id, data):
    """게시글 작성"""
    format_data = json.loads(data)
    format_data['board_id'] = board_id

    result = PostCreateSchema().load(format_data)
    result.save()


def editPost(post_id, data):
    return None


def deletePost(post_id):
    return None