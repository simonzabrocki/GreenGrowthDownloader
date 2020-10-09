import pkg_resources
import json


def load_API_params(API_name):
    """
    """
    # This is a stream-like object. If you want the actual info, call
    stream = pkg_resources.resource_stream(__name__, f'params/{API_name}.json')
    with open(stream.name, 'r') as f:
        data = json.load(f)
    return data
