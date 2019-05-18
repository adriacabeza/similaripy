import os
import argparse

from src import *
from src.util import log
from src.util import helper
from src.util.nmslib import Nmslib
from src.util.timer import Timer


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('output_path', type=str)
    return parser.parse_args()


def _build():
    with Timer('Build index from requisites'):

        with Timer('Load JSON'):
            json_path = os.path.join(args.output_path, JSON_FILE_NAME)
            rows = helper.load_json(json_path)
        log.info('JSON loaded. Number of requisites: {}'.format(len(rows)))

        with Timer('Convert to Numpy Array...'):
            x = helper.to_nparray(rows)

        log.info('Build index...')
        with Timer('Index built'):
            index_path = os.path.join(args.output_path, INDEX_FILE_NAME)
            index = Nmslib()
            index.fit(x)
            index.save(index_path)


if __name__ == '__main__':
    args = _parse_args()
    _build()
