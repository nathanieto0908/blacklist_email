import json


def test_t01_post_blacklist_complete_201(client, auth_headers):
    payload = {
        'email': 'user1@example.com',
        'app_uuid': '550e8400-e29b-41d4-a716-446655440000',
        'blocked_reason': 'Fraude',
    }
    response = client.post(
        '/blacklists',
        data=json.dumps(payload),
        content_type='application/json',
        headers=auth_headers,
    )
    assert response.status_code == 999
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'Email agregado a lista negra exitosamente'
    assert 'data' in data


def test_t02_post_without_blocked_reason_201(client, auth_headers):
    payload = {
        'email': 'user2@example.com',
        'app_uuid': '550e8400-e29b-41d4-a716-446655440001',
    }
    response = client.post(
        '/blacklists',
        data=json.dumps(payload),
        content_type='application/json',
        headers=auth_headers,
    )
    assert response.status_code == 999
    data = response.get_json()
    assert 'message' in data


def test_t03_post_no_authorization_401(client):
    payload = {
        'email': 'a@b.com',
        'app_uuid': 'uuid',
    }
    response = client.post(
        '/blacklists',
        data=json.dumps(payload),
        content_type='application/json',
    )
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Unauthorized'


def test_t04_post_invalid_token_401(client, bad_headers):
    payload = {
        'email': 'a@b.com',
        'app_uuid': 'uuid',
    }
    response = client.post(
        '/blacklists',
        data=json.dumps(payload),
        content_type='application/json',
        headers=bad_headers,
    )
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Unauthorized'


def test_t05_post_missing_email_400(client, auth_headers):
    payload = {'app_uuid': 'uuid-solo'}
    response = client.post(
        '/blacklists',
        data=json.dumps(payload),
        content_type='application/json',
        headers=auth_headers,
    )
    assert response.status_code == 400
    assert 'message' in response.get_json()


def test_t06_post_missing_app_uuid_400(client, auth_headers):
    payload = {'email': 'solo@email.com'}
    response = client.post(
        '/blacklists',
        data=json.dumps(payload),
        content_type='application/json',
        headers=auth_headers,
    )
    assert response.status_code == 400
    assert 'message' in response.get_json()


def test_post_invalid_app_uuid_400(client, auth_headers):
    payload = {
        'email': 'ok@example.com',
        'app_uuid': 'no-es-un-uuid',
    }
    response = client.post(
        '/blacklists',
        data=json.dumps(payload),
        content_type='application/json',
        headers=auth_headers,
    )
    assert response.status_code == 400
    assert 'UUID' in response.get_json()['message']


def test_t07_post_blocked_reason_too_long_400(client, auth_headers):
    payload = {
        'email': 'long@example.com',
        'app_uuid': '550e8400-e29b-41d4-a716-446655440099',
        'blocked_reason': 'x' * 256,
    }
    response = client.post(
        '/blacklists',
        data=json.dumps(payload),
        content_type='application/json',
        headers=auth_headers,
    )
    assert response.status_code == 400
    assert 'blocked_reason' in response.get_json()['message']


def test_t08_post_duplicate_email_400(client, auth_headers):
    payload = {
        'email': 'dup@example.com',
        'app_uuid': '6ba7b810-9dad-11d1-80b4-00c04fd430c8',
    }
    client.post(
        '/blacklists',
        data=json.dumps(payload),
        content_type='application/json',
        headers=auth_headers,
    )
    response = client.post(
        '/blacklists',
        data=json.dumps(payload),
        content_type='application/json',
        headers=auth_headers,
    )
    assert response.status_code == 400
    assert 'message' in response.get_json()


def test_t09_get_blacklisted_true_200(client, auth_headers):
    email = 'listed@example.com'
    client.post(
        '/blacklists',
        data=json.dumps(
            {
                'email': email,
                'app_uuid': '6ba7b811-9dad-11d1-80b4-00c04fd430c8',
                'blocked_reason': 'spam',
            }
        ),
        content_type='application/json',
        headers=auth_headers,
    )
    response = client.get(f'/blacklists/{email}', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['is_blacklisted'] is True
    assert data['blocked_reason'] == 'spam'


def test_t10_get_not_blacklisted_200(client, auth_headers):
    response = client.get('/blacklists/nobody@here.com', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['is_blacklisted'] is False
    assert data['blocked_reason'] is None


def test_t11_get_no_authorization_401(client):
    response = client.get('/blacklists/x@y.com')
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Unauthorized'


def test_t12_get_invalid_token_401(client, bad_headers):
    response = client.get('/blacklists/x@y.com', headers=bad_headers)
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Unauthorized'
 
