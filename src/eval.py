import argparse
import json

from tqdm import tqdm

from src.util import log
from src.util.timer import Timer


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('validation_duplicates_file', type=str)
    parser.add_argument('clusters_file', type=str)
    return parser.parse_args()


def _chunks(l, n):
    return list(zip(*[iter(l)] * n))


def _eval_dup(dup, clusters):
    for cluster in clusters:
        if set(dup).issubset(cluster):
            return True
    return False


def get_matrix():
    with Timer('Compute accuracy'):

        with Timer('Load Validation duplicates JSON'):
            with open(args.validation_duplicates_file) as f:
                duplicates_requisites = json.load(f)
                duplicates_requisites = duplicates_requisites['requirements']
                duplicates_requisites = _chunks(duplicates_requisites, 2)

        with Timer('Load clusters JSON'):
            with open(args.clusters_file) as f:
                clusters = json.load(f)

        with Timer('Eval clusters'):
            correct = 0
            total_groups = len(duplicates_requisites)
            for dup in tqdm(duplicates_requisites, total=total_groups):
                correct += _eval_dup(dup, clusters)
            accuracy = (correct / total_groups) * 100

    log.info('ACCURACY: {}%'.format(accuracy))


if __name__ == '__main__':
    args = _parse_args()
    get_matrix()
