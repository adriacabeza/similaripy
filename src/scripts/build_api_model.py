import argparse
import json
import requests

from src import *


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_requirements_file', type=str)
    return parser.parse_args()


def build_api_model():
    with open(args.input_requirements_file) as f:
        data = json.load(f)

    params = {'organization': 'UPC'}
    response = requests.post(BUILD_MODEL_ENDPOINT, params=params, json=data)
    print('Status code: {}'.format(response.status_code))


if __name__ == '__main__':
    args = _parse_args()
    build_api_model()
