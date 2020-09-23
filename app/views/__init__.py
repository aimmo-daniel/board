from flask import jsonify

from app.views.auth import AuthView
from app.views.board import BoardView
from app.views.comment import CommentView
from app.views.member import MemberView
from app.views.post import PostView


def json_decoder_error(e):
    return jsonify(message='Json decoder 오류'), 400


def handle_bad_request(e):
    return jsonify(message='잘못된 요청입니다.'), 400


def handle_not_found(e):
    return jsonify(message='페이지를 찾을 수 없습니다.'), 404


def register_error_handlers(blueprint):
    blueprint.register_error_handler(400, json_decoder_error)
    blueprint.register_error_handler(400, handle_bad_request)
    blueprint.register_error_handler(404, handle_not_found)


def register_api(app):
    name_space = '/api/v1/'

    AuthView.register(app, route_base=name_space + 'auth', trailing_slash=False)
    MemberView.register(app, route_base=name_space + 'member', trailing_slash=False)
    BoardView.register(app, route_base=name_space + 'board', trailing_slash=False)
    PostView.register(app, route_base=name_space + 'board/<board_id>/post', trailing_slash=False)
    CommentView.register(app, route_base=name_space + 'board/<board_id>/post/<post_id>/comment', trailing_slash=False)

    register_error_handlers(app)