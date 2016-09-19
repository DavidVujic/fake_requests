import os
import requests
import json
from xml.etree import ElementTree

original_get = requests.get
original_post = requests.post
original_delete = requests.delete


def fake_request_maker():
    def setup_fake_requests():
        def make_fake_call(url, *args, **kwargs):
            data, status_code = responses.pop(0)
            return FakeHttpResponse(data, status_code)

        requests.get = make_fake_call
        requests.post = make_fake_call
        requests.delete = make_fake_call

    def add(expected_response):
        if isinstance(expected_response, tuple):
            to_append = expected_response
        else:
            to_append = (expected_response, 200)

        responses.append(to_append)

    responses = []
    setup_fake_requests()

    return add


def reset():
    requests.get = original_get
    requests.post = original_post
    requests.delete = original_delete


class FakeHttpResponse:

    def __init__(self, message, status_code):
        self.text = message
        self.content = message
        self.status_code = status_code

    def json(self):
        return self.text

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError('Error!', response=self)
