from nose.tools import assert_equal

from examples.src import example
from fake_requests import fake_response, reset

_fake_response = None


def teardown():
    reset()


def test_download_stats():
    fake_response({'message': 'hello world'})
    fake_response({'message': 'goodbye world'})

    result = example.get_data('my-fake-url')
    result2 = example.get_data('my-fake-url-2')

    assert_equal(result, 'hello world')
    assert_equal(result2, 'goodbye world')
