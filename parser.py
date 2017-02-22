import json
from xml.etree import ElementTree


def fake_data_from(file_path, file_format='json'):
    with open(file_path) as f:
        if file_format == 'json':
            expected = json.load(f)
        elif file_format == 'xml':
            expected = ElementTree.parse(f)
        else:
            expected = f.read()

    return expected
