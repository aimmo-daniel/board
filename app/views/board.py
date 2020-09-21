from flask import jsonify, request
from flask_classful import FlaskView, route

from app.service import boardService


class BoardView(FlaskView):
    @route('', methods=['GET'])
    def list(self):
        board_list = boardService.boardList()
        return jsonify(board_list), 200

    @route('/<board_id>', methods=['GET'])
    def detail(self, board_id, page=1):
        board_detail = boardService.boardDetail(board_id, page)
        return jsonify(board_detail), 200

    @route('', methods=['POST'])
    def create(self):
        boardService.createBoard(request.data)
        return jsonify(message='게시판이 생성되었습니다.'), 200

    @route('/<board_id>', methods=['PUT'])
    def edit(self, board_id):
        boardService.editName(board_id, request.data)
        return jsonify(message='게시판 이름이 변경되었습니다.'), 200

    @route('/<board_id>', methods=['DELETE'])
    def delete(self, board_id):
        boardService.deleteBoard(board_id)
        return jsonify(message='게시판이 삭제되었습니다.'), 200