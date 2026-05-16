from datetime import timedelta

import jwt

from api.auth import ALGORITHM, SECRET_KEY, create_access_token


def test_create_access_token_contains_sub():
    token = create_access_token({'sub': 'viewer'}, expires_delta=timedelta(minutes=5))
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload['sub'] == 'viewer'
    assert 'exp' in payload
