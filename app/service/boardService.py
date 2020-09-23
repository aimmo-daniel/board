import json
from collections import OrderedDict

from flask import jsonify, current_app

from app.models.board import Board
from app.models.post import Post
from app.serializers.board import BoardSchema, BoardDetailSchema
from app.serializers.post import PostSchema


def boardList():
    # 게시판 목록 조회
    boards = Board.objects(deleted=False)
    result = BoardSchema().dump(boards, many=True)
    return result


def boardDetail(board_id):
    # 게시판의 게시글 목록 조회
    find_board = Board.objects(id=board_id).get()
    board_info = BoardSchema(exclude={'deleted'}).dump(find_board)

    find_post_list = Post.objects(board=board_id, deleted=False).order_by('+create_time', '-like_count')
    post_list = PostSchema(exclude={'board', 'deleted', 'writer.deleted', 'writer.create_time', 'writer.last_login'}).dump(find_post_list, many=True)

    result = OrderedDict()
    result['board'] = board_info
    result['post_list'] = post_list

    # Json 변환시에도 OrderDict 순서 보장
    response = current_app.response_class(json.dumps(result, sort_keys=False), mimetype=current_app.config['JSONIFY_MIMETYPE'])

    return response


def createBoard(data):
    # 게시판 생성
    format_data = json.loads(data)
    request_name = format_data['name']

    if Board.objects(name=request_name):
        return jsonify(message='이미 존재하는 게시판 이름입니다.'), 409

    result = BoardSchema().load(format_data)
    result.save()


def editName(board_id, data):
    # 게시판 이름 수정
    format_data = json.loads(data)
    request_name = format_data['name']

    if Board.objects(name=request_name):
        return jsonify(message='이미 존재하는 게시판 이름입니다.'), 409

    find_board = Board.objects(id=board_id)
    find_board.edit_name(request_name)


def deleteBoard(board_id):
    # 게시판 삭제
    find_board = Board.objects(id=board_id)
    find_board.soft_delete()