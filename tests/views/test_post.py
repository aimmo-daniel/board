import json
import uuid

import pytest
from bson import ObjectId
from faker import Faker
from flask import url_for

from app.models.post import Post
from tests.factories.board import BoardFactory, DeletedBoardFactory
from tests.factories.member import MemberFactory
from tests.factories.post import PostFactory, DeletedPostFactory


class Describe_PostView:
    @pytest.fixture
    def board(self):
        return BoardFactory.create()

    @pytest.fixture
    def logged_in_member(self):
        return MemberFactory.create()

    @pytest.fixture
    def post(self, board, logged_in_member):
        return PostFactory.create(board=board.id, writer=logged_in_member.id)

    class Describe_index:
        @pytest.fixture(autouse=True)
        def subject(self, client, headers, post):
            url = url_for('PostView:index', board_id=post.board.id, post_id=post.id)
            return client.get(url, headers=headers)

        class Context_정상_요청:
            def test_200이_반환된다(self, subject):
                assert subject.status_code == 200

            def test_게시글_목록이_반환된다(self, subject, post):
                body = subject.get_json()
                assert body[0]['id'] == str(post.id)

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

            class Context_로그인하지_않은경우:
                @pytest.fixture
                def token(self):
                    return ObjectId()

                def test_401이_반환된다(self, subject):
                    assert subject.status_code == 401

    class Describe_get:
        @pytest.fixture(autouse=True)
        def subject(self, client, headers, post):
            url = url_for('PostView:get', board_id=post.board.id, post_id=post.id)
            return client.get(url, headers=headers)

        class Context_정상요청:
            def test_200이_반환된다(self, subject):
                assert subject.status_code == 200

            def test_게시글이_조회된다(self, subject, post):
                assert subject.json['id'] == str(post.id)

        class Context_게시판이_없는경우:
            @pytest.fixture
            def board(self):
                return DeletedBoardFactory.create()

            def test_404가_반환된다(self, subject):
                assert subject.status_code == 404

        class Context_게시글이_없는경우:
            @pytest.fixture
            def post(self):
                return DeletedPostFactory.create()

            def test_404가_반환된다(self, subject):
                assert subject.status_code == 404

        class Context_로그인하지_않은경우:
            @pytest.fixture
            def token(self):
                return ObjectId()

            def test_401이_반환된다(self, subject):
                assert subject.status_code == 401

    class Describe_post:
        @pytest.fixture
        def form(self):
            fake = Faker()
            return {
                "title": fake.name(),
                "content": fake.name(),
                "tags": ["tags"]
            }

        @pytest.fixture(autouse=True)
        def subject(self, client, headers, form, board):
            url = url_for('PostView:post', board_id=board.id)
            return client.post(url, headers=headers, data=json.dumps(form))

        class Context_정상요청:
            def test_200이_반환된다(self, subject):
                assert subject.status_code == 200

            def test_게시글이_추가된다(self, subject, form, logged_in_member):
                assert Post.objects.count() == 1
                post = Post.objects.first()
                assert post.title == form['title']
                assert post.content == form['content']
                assert post.tags == form['tags']
                assert post.writer.id == logged_in_member.id

        class Context_요청이_유효하지_않은경우:

            class Context_title이_없는경우:
                @pytest.fixture
                def form(self, form):
                    form['title'] = None
                    return form

                def test_422가_반환된다(self, subject):
                    assert subject.status_code == 422

            class Context_tag의_type이_str이_아닌경우:
                @pytest.fixture
                def form(self, form):
                    form['tags'] = 12345
                    return form

                def test_422가_반환된다(self, subject):
                    assert subject.status_code == 422

        class Context_로그인하지_않은경우:
            @pytest.fixture
            def post(self, board):
                return PostFactory.create(board=board.id)

            @pytest.fixture
            def logged_in_member(self):
                return None

            def test_401이_반환된다(self, subject):
                assert subject.status_code == 401

            class Context_유효하지_않은_토큰경우:
                @pytest.fixture
                def token(self):
                    return uuid.uuid4()

                def test_401이_반환된다(self, subject):
                    assert subject.status_code == 401

        class Context_존재하지_않는_게시판에_게시글을_생성할경우:
            @pytest.fixture
            def board(self):
                return DeletedBoardFactory.create()

            def test_404가_반환된다(self, subject):
                assert subject.status_code == 404
