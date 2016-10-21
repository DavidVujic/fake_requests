import requests

_original_get = requests.get
_original_post = requests.post
_original_delete = requests.delete
_original_session = requests.Session

_responses = []


def fake_request_maker():
    def add(expected_response, status_code=200):
        _responses.append((expected_response, status_code))

    requests.get = _fake_call
    requests.post = _fake_call
    requests.delete = _fake_call
    requests.Session = FakeSession
    requests.session = FakeSession

    return add


def reset():
    requests.get = _original_get
    requests.post = _original_post
    requests.delete = _original_delete
    requests.Session = _original_session
    requests.session = _original_session

    global _responses
    _responses = []


class FakeSession:
    def __init__(self):
        self.get = _fake_call
        self.post = _fake_call
        self.delete = _fake_call


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


def _fake_call(url, *args, **kwargs):
    data, status_code = _responses.pop(0)
    return FakeHttpResponse(data, status_code)
