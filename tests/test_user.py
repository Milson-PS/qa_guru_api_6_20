import os
import json

import pytest
import requests
from jsonschema.validators import validate


def test_users_list_status():
    r = requests.get(url='https://reqres.in/api/users')

    assert r.status_code == requests.codes.ok


def test_create_user():
    r = requests.post(url='https://reqres.in/api/users',
                      data={'name': 'morpheus', 'job': 'leader'})
    assert r.status_code == requests.codes.created
    assert all(key in r.json() for key in ['id', 'name', 'job', 'createdAt'])


def test_modify_user():
    r = requests.patch(url='https://reqres.in/api/users/2',
                       data={'job': 'zion resident'})

    assert r.status_code == requests.codes.ok
    assert all(key in r.json() for key in ['job', 'updatedAt'])


def test_delete_user():
    r = requests.delete(url='https://reqres.in/api/users/2')

    assert r.status_code == requests.codes.no_content
    assert r.text == ''


def test_single_user_status_code():
    r = requests.get(url='https://reqres.in/api/users/1')

    assert r.status_code == requests.codes.ok


def test_single_users_schema():
    path_to_schema = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            'resources/single_users_schema.json'
        )
    )
    with open(path_to_schema) as file:
        schema = json.loads(file.read())

        r = requests.get(url='https://reqres.in/api/users/1')

        validate(instance=r.json(), schema=schema)


@pytest.mark.parametrize('per_page', [0, 'abcd', '_%$#-'])
def test_us_list(per_page):
    default_per_page = 6

    r = requests.get(url='https://reqres.in/api/users',
                     params={'per_page': per_page})
    assert r.json()['per_page'] == default_per_page
    assert len(r.json()['data']) == default_per_page


def test_users_list_empty_page():
    r = requests.get(url='https://reqres.in/api/users')
    total = r.json()['total']

    r = requests.get(url='https://reqres.in/api/users',
                     params={'per_page': total, 'page': 2})

    assert r.json()['data'] == []
