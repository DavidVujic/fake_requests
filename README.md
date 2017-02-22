### Fake Requests
A simple helper for unit testing modules that use the requests library.

The fake_requests module uses monkey patching to make fake http requests. This is useful when writing unit tests for code that uses explicit imports.

#### Example usage
```python
from fake_requests import add_fake_response, reset
from parser import fake_data_from

def test_my_example_unit_test():
  # arrange: add one or more fake responses
  add_fake_response('{"data": "this is a fake response"}')

  # or load a file with fake data
  add_fake_response(fake_data_from('fake.json'))

  # act: run the code to be tested
  result = my_module.run_some_code()

  # assert
  assert_equal(result.get('data'), "data that my_module has parsed")

  # teardown
  reset()

```
