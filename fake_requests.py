import requests


class FakeRequests():
    def __init__(self):
        self.responses = []
        self.is_initialized = False

    def init(self, req_lib=None):
        if not req_lib:
            req_lib = requests

        req_lib.get = self.fake_call
        req_lib.post = self.fake_call
        req_lib.delete = self.fake_call
        req_lib.Session = FakeSession

        self.is_initialized = True

    def reset(self, req_lib=None):
        if not req_lib:
            req_lib = requests

        self.responses = []
        self.is_initialized = False
        reload(req_lib)

    def response(self, expected_response, status_code=200):
        if not self.is_initialized:
            self.init()

        self.responses.append((expected_response, status_code))

    def fake_call(self, url, *args, **kwargs):
        data, status_code = self.responses.pop(0)
        return FakeHttpResponse(data, status_code)


class FakeSession:
    def __init__(self, fake):
        self.get = fake.fake_call
        self.post = fake.fake_call
        self.delete = fake.fake_call
        self.request = fake.fake_call


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
