import os
import argparse
import json

from tqdm import tqdm

from src import *
from src.util import log
from src.util import helper
from src.util.nmslib import Nmslib


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_path', type=str)
    return parser.parse_args()


def _search(index):
    log.info('Loading JSON...')
    json_path_score = os.path.join(args.data_path, JSON_FILE_NAME)
    json_path_mapping = os.path.join(args.data_path, MAPPING_FILE_NAME)
    mapping = helper.load_json(json_path_mapping)
    score_matrix = helper.load_json(json_path_score)
    clusters = {}
    next_id = 0
    req_to_cl = {}

    pbar = tqdm(total= len(score_matrix))
    for i, embd in enumerate(score_matrix):
        embd = helper.to_nparray(embd)
        closest, distances = index.query(embd, NEIGHBOURHOOD_AMOUNT)

        similar = {i}
        for j, dist in zip(closest, distances):
            if j != i:
                if dist < DISTANCE_THRESHOLD:
                    similar.add(int(j))

        # merge clusters with previously found if possible
        matching_clusters = set()
        for j in similar:
            if j in req_to_cl:
                matching_clusters.add(req_to_cl[j])

        for cl in matching_clusters:
            similar.update(clusters.pop(cl))

        # add new cluster to list
        cl_id = next_id
        next_id += 1

        clusters[cl_id] = similar
        for j in similar:
            req_to_cl[j] = cl_id
        
        pbar.update(1)
    
    return list(clusters)


def find_clusters():
    index = Nmslib()
    index.load(fn=os.path.join(args.data_path, INDEX_FILE_NAME))
    clusters = _search(index)
    with open(os.path.join(OUTPUT_PATH, 'clusters.json'), 'w') as f:
        json.dump(clusters, f)


if __name__ == '__main__':
    args = _parse_args()
    find_clusters()
