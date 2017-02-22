from nose.tools import assert_equal

from examples.src import example
from fake_requests import fake_request_maker, reset

fake_response = None


def setup():
    global fake_response
    fake_response = fake_request_maker()


def teardown():
    reset()


def test_download_stats():
    global fake_response

    fake_response({'message': 'hello world'})

    result = example.get_data('my-fake-url')

    assert_equal(result, 'hello world')
