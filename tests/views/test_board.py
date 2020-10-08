import json

import pytest
from bson import ObjectId
from faker import Faker
from flask import url_for

from app.models.board import Board
from tests.factories.board import BoardFactory, DeletedBoardFactory
from tests.factories.member import MemberFactory


class Describe_BoardView:
    @pytest.fixture
    def logged_in_member(self):
        return MemberFactory.create()

    class Describe_index:
        @pytest.fixture
        def already_created_board(self):
            return BoardFactory.create()

        @pytest.fixture
        def subject(self, client, headers, already_created_board):
            url = url_for('BoardView:index')
            return client.get(url)

        class Context_정상_요청:
            def test_200이_반환된다(self, subject):
                assert subject.status_code == 200

            def test_게시판_목록이_반환된다(self, subject, already_created_board):
                body = subject.get_json()
                assert body[0]['id'] == str(already_created_board.id)
                assert body[0]['name'] == already_created_board.name

        class Context_Board가_없는경우:
            @pytest.fixture
            def already_created_board(self):
                return None

            def test_200이_반환된다(self, subject):
                assert subject.status_code == 200

            def test_빈값이_반환된다(self, subject, already_created_board):
                body = subject.get_json()
                assert body == []

        class Context_삭제된_게시판일_경우:
            @pytest.fixture
            def already_created_board(self):
                return DeletedBoardFactory.create()

            def test_200이_반환된다(self, subject):
                assert subject.status_code == 200

            def test_빈값이_반환된다(self, subject, already_created_board):
                body = subject.get_json()
                assert body == []

    class Describe_get:
        @pytest.fixture
        def already_created_board(self):
            return BoardFactory.create()

        @pytest.fixture
        def target_board_id(self, already_created_board):
            return already_created_board.id

        @pytest.fixture
        def subject(self, client, target_board_id):
            url = url_for('BoardView:get', board_id=target_board_id)
            return client.get(url)

        class Context_정상케이스:
            def test_200이_반환된다(self, subject):
                assert subject.status_code == 200

            def test_board가_반환된다(self, subject, already_created_board):
                body = subject.get_json()

                assert body['id'] == str(already_created_board.id)
                assert body['name'] == already_created_board.name
                assert body['deleted'] == already_created_board.deleted

        class Context_존재하지않는_board_id인경우:
            @pytest.fixture
            def target_board_id(self):
                return ObjectId()
            # Todo: 수정하기
            def test_404이_반환된다(self, subject):
                assert subject.status_code == 404

    class Describe_post:
        @pytest.fixture
        def form(self):
            fake = Faker()
            return {'name': fake.name()}

        @pytest.fixture
        def subject(self, client, headers, form):
            url = url_for('BoardView:post')
            return client.post(url, headers=headers, data=json.dumps(form))

        class Context_정상_요청:
            def test_200이_반환된다(self, subject):
                assert subject.status_code == 200

            def test_db에_저장된다(self, subject, form):
                board = Board.objects(name=form['name']).get()
                assert board.name == form['name']

        class Context_name이_입력되지_않은경우:
            @pytest.fixture
            def form(self):
                return {'name': None}

            def test_422가_반환된다(self, subject):
                assert subject.status_code == 422

        class Context_게시판명이_중복되는_경우:
            @pytest.fixture
            def already_exist_board(self):
                return BoardFactory.create()

            @pytest.fixture
            def form(self, already_exist_board):
                return {'name': already_exist_board.name}

            def test_409가_반환된다(self, subject):
                assert subject.status_code == 409

        class Context_로그인을_하지_않은경우:
            @pytest.fixture
            def token(self):
                return None

            def test_401이_반환된다(self, subject):
                assert subject.status_code == 401

    class Describe_put:
        @pytest.fixture
        def already_created_board(self):
            return BoardFactory.create()

        @pytest.fixture
        def target_board_id(self, already_created_board):
            return already_created_board.id

        @pytest.fixture
        def form(self):
            fake = Faker()
            return {'name': fake.name()}

        @pytest.fixture
        def subject(self, client, headers, form, target_board_id):
            url = url_for('BoardView:put', board_id=target_board_id)
            return client.put(url, headers=headers, data=json.dumps(form))

        class Context_정상_요청:
            def test_200이_반환된다(self, subject):
                assert subject.status_code == 200

            def test_name이_변경된다(self, subject, target_board_id, form):
                board = Board.objects(id=target_board_id).get()
                assert board.name == form['name']

        class Context_name이_입력되지_않은경우:
            @pytest.fixture
            def form(self):
                return {'name': None}

            def test_422가_반환된다(self, subject):
                assert subject.status_code == 422

        class Context_게시판명이_중복되는_경우:
            @pytest.fixture
            def already_exist_board(self):
                return BoardFactory.create()

            @pytest.fixture
            def form(self, already_exist_board):
                return {'name': already_exist_board.name}

            def test_409가_반환된다(self, subject):
                assert subject.status_code == 409

        class Context_로그인을_하지_않은경우:
            @pytest.fixture
            def token(self):
                return None

            def test_401이_반환된다(self, subject):
                assert subject.status_code == 401

    class Describe_delete:
        @pytest.fixture
        def already_created_board(self):
            return BoardFactory.create()

        @pytest.fixture
        def subject(self, client, headers, already_created_board):
            url = url_for('BoardView:delete', board_id=already_created_board.id)
            return client.delete(url, headers=headers)

        class Context_정상케이스:
            def test_200이_반환된다(self, subject):
                assert subject.status_code == 200

            def test_board의_deleted가_True가_된다(self, subject):
                board_is_deleted = Board.objects.get().deleted
                assert board_is_deleted is True

        class Context_로그인하지_않은경우:
            @pytest.fixture
            def token(self):
                return None

            def test_401이_반환된다(self, subject):
                assert subject.status_code == 401
