import os
import argparse

from src import *
from src.util import log
from src.util import helper
from src.util.nmslib import Nmslib


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('output_path', type=str)
    return parser.parse_args()


def _build():
    log.info('Loading JSON...')
    json_path = os.path.join(args.output_path, JSON_FILE_NAME)
    rows = helper.load_json(json_path)
    log.info('JSON loaded. Number of requisites: {}'.format(len(rows)))

    log.info('Converting to Numpy Array...')
    x = helper.to_nparray(rows)
    log.info('Converted')

    log.info('Building index...')
    index_path = os.path.join(args.output_path, INDEX_FILE_NAME)
    index = Nmslib()
    index.fit(x)
    index.save(index_path)
    log.info('Index built')


if __name__ == '__main__':
    args = _parse_args()
    _build()
