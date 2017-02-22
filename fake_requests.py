import requests

_original_get = None
_original_post = None
_original_delete = None
_original_session = None

_responses = []


def fake_request_maker(req_lib=None):
    def add(expected_response, status_code=200):
        _responses.append((expected_response, status_code))

    if not req_lib:
        req_lib = requests

    _keep_original_functions(req_lib)

    req_lib.get = _fake_call
    req_lib.post = _fake_call
    req_lib.delete = _fake_call
    req_lib.Session = FakeSession

    return add


def reset(req_lib=None):
    if not req_lib:
        req_lib = requests

    req_lib.get = _original_get
    req_lib.post = _original_post
    req_lib.delete = _original_delete
    req_lib.Session = _original_session

    global _responses
    _responses = []


class FakeSession:
    def __init__(self):
        self.get = _fake_call
        self.post = _fake_call
        self.delete = _fake_call
        self.request = _fake_call


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


def _keep_original_functions(req_lib):
    global _original_get, _original_post, _original_delete, _original_session
    _original_get = req_lib.get
    _original_post = req_lib.post
    _original_delete = req_lib.delete
    _original_session = req_lib.Session
