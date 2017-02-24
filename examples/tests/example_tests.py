from nose.tools import assert_equal

from examples.src import example
from fake_requests import FakeRequests

fake = FakeRequests()


def teardown():
    fake.reset()


def test_download_stats():
    fake.response({'message': 'hello world'})
    fake.response({'message': 'goodbye world'})

    result = example.get_data('my-fake-url')
    result2 = example.get_data('my-fake-url-2')

    assert_equal(result, 'hello world')
    assert_equal(result2, 'goodbye world')
