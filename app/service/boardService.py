import json

from flask import jsonify

from app.models.board import Board
from app.serializers.board import BoardSchema, BoardDetailSchema


def boardList():
    """게시판 목록 조회"""
    boards = Board.objects(deleted=False)
    result = BoardSchema().dump(boards, many=True)
    return result


def boardDetail(board_id):
    """게시판 게시물 정보 조회"""
    find_board = Board.objects(id=board_id).get()
    result = BoardDetailSchema().dump(find_board)
    return result


def createBoard(data):
    """게시판 생성"""
    format_data = json.loads(data)

    if Board.objects(name=format_data['name']):
        return jsonify(message='이미 존재하는 게시판 이름입니다.'), 409

    result = BoardSchema().load(format_data)
    result.save()


def editName(board_id, data):
    """게시판 이름 수정"""
    format_data = json.loads(data)

    if Board.objects(name=format_data['name']):
        return jsonify(message='이미 존재하는 게시판 이름입니다.'), 409

    find_board = Board.objects(id=board_id)
    find_board.update(name=format_data['name'])


def deleteBoard(board_id):
    """게시판 삭제"""
    find_board = Board.objects(id=board_id)
    find_board.update(deleted=True)