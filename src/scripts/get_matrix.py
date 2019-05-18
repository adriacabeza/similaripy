import argparse
import json
import requests

from src import *


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_duplicates_file', type=str)
    parser.add_argument('output_mapping_file', type=str)
    parser.add_argument('output_matrix_file', type=str)
    return parser.parse_args()


def get_matrix():
    with open(args.input_duplicates_file) as f:
        data = json.load(f)

    params = {'organization': 'UPC', 'threshold': 0.1}
    response = requests.post(COMPUTE_CLUSTERS_ENDPOINT, params=params, json=data)
    response_matrix = response.json()['dependencies']

    assert len(response_matrix) == len(data['requirements'])

    mapping_dict = {}
    for idx, req in enumerate(data['requirements']):
        mapping_dict[idx] = req
    with open(args.output_matrix_file, 'w') as f:
        json.dump(mapping_dict, f)

    with open(args.output_mapping_file, 'w') as f:
        json.dump(response_matrix, f)


if __name__ == '__main__':
    args = _parse_args()
    get_matrix()
