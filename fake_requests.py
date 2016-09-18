import os
import requests
import json
from xml.etree import ElementTree


class FakeRequests:

    def __init__(self):
        self.responses = []
        self.original_get = requests.get
        self.original_post = requests.post
        self._setup_requests()

    def _setup_requests(self):
        def fake_call(url, *args, **kwargs):
            data, status_code = self.responses.pop(0)
            return FakeHttpResponse(data, status_code)

        requests.get = fake_call
        requests.post = fake_call
        requests.delete = fake_call

    def add(self, expected_response):
        if isinstance(expected_response, tuple):
            to_append = expected_response
        else:
            to_append = (expected_response, 200)

        self.responses.append(to_append)

    def reset(self):
        requests.get = self.original_get
        requests.post = self.original_post
        self.responses = []


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
