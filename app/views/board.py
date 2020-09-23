from flask import jsonify, request
from flask_classful import FlaskView, route

from app.service import boardService
from app.utils import auth_required


class BoardView(FlaskView):
    @route('', methods=['GET'])
    def list(self):
        board_list = boardService.boardList()
        return jsonify(board_list), 200

    @route('/<board_id>', methods=['GET'])
    @auth_required
    def detail(self, board_id):
        board_detail = boardService.boardDetail(board_id)
        return board_detail

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