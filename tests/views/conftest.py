import jwt
import pytest

from flask import current_app
from bson.json_util import dumps as bson_dumps


@pytest.fixture
def token(logged_in_member):
    if logged_in_member:
        return jwt.encode({"member_id": bson_dumps(logged_in_member.id)},
                       current_app.config['SECRET'],
                       current_app.config['ALGORITHM'])
    else:
        return None

@pytest.fixture
def headers(token):
    if token:
        headers = {
            'Authorization': token
        }
    else:
        headers = None
    return headers