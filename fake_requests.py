import requests

_responses = []
_is_initialized = False


def add_fake_response(expected_response, status_code=200):
    if not _is_initialized:
        init()
    _responses.append((expected_response, status_code))


def init(req_lib=None):
    if not req_lib:
        req_lib = requests

    req_lib.get = _fake_call
    req_lib.post = _fake_call
    req_lib.delete = _fake_call
    req_lib.Session = FakeSession


def reset(req_lib=None):
    global _responses
    global _is_initialized

    if not req_lib:
        req_lib = requests

    reload(req_lib)

    _responses = []
    _is_initialized = False


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
