import os
import argparse
import json
import numpy as np

from tqdm import tqdm


from src import *
from src.util import log
from src.util import helper
from src.util.nmslib import Nmslib
from src.util.timer import Timer


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_path', type=str)
    return parser.parse_args()


def _search(index):
    with Timer('Load JSON'):
        json_path_score = os.path.join(args.data_path, JSON_FILE_NAME)
        json_path_mapping = os.path.join(args.data_path, MAPPING_FILE_NAME)
        mapping = helper.load_json(json_path_mapping)
        score_matrix = helper.load_json(json_path_score)

    clusters = {}
    next_id = 0
    req_to_cl = {}
    progress_bar = tqdm(total=len(score_matrix))
    for i, vector_arrays in enumerate(score_matrix):
        vector_arrays = helper.to_nparray(vector_arrays)
        closest, distances = index.query(vector_arrays, NEIGHBOURHOOD_AMOUNT)

        similar = {i}
        for j, dist in zip(closest, distances):
            if j != i:
                if dist < DISTANCE_THRESHOLD:
                    similar.add(int(j))

        matching_clusters = set()
        for j in similar:
            if j in req_to_cl:
                matching_clusters.add(req_to_cl[j])

        for cl in matching_clusters:
            similar.update(clusters.pop(cl))

        cl_id = next_id
        next_id += 1

        clusters[cl_id] = similar
        for j in similar:
            req_to_cl[j] = cl_id

        progress_bar.update(1)

    similar_clusters = [list(cl) for cl in clusters.values()]
    for i in range(0, len(similar_clusters)):
        for j in range(0, len(similar_clusters[i])):
            similar_clusters[i][j] = mapping[str(similar_clusters[i][j])]
    
    return similar_clusters


def _metrics(clusters):
    log.info('METRICS')

    total_requirements = int(np.concatenate(clusters).shape[0])
    log.info('Total requirements: {}'.format(total_requirements))

    dup_clusters = list(filter(lambda x: len(x) > 1, clusters))
    dup_requirements = int(np.concatenate(dup_clusters).shape[0]) if dup_clusters else 0
    log.info('Similar requirements: {}'.format(dup_requirements))

    unique_requirements = total_requirements - dup_requirements
    log.info('Unique requirements: {}'.format(unique_requirements))

    avg_cluster_size = float(np.mean(list(map(len, dup_clusters)))) if dup_requirements else 0
    log.info('Average cluster size (for size > 1): {}'.format(avg_cluster_size))

    max_cluster_size = int(np.max(list(map(len, dup_clusters)))) if dup_requirements else 0
    log.info('Maximum cluster size: {}'.format(max_cluster_size))

    similar_pct = (dup_requirements / total_requirements) * 100
    log.info('Percentage of duplicates: {}%'.format(similar_pct))

    amount_clusters = len(clusters)
    log.info('Amount of clusters: {}'.format(amount_clusters))


def find_clusters():
    index = Nmslib()
    index.load(fn=os.path.join(args.data_path, INDEX_FILE_NAME))
    clusters = _search(index)
    with open(os.path.join(OUTPUT_PATH, 'clusters.json'), 'w') as f:
        json.dump(clusters, f)
    _metrics(clusters)


if __name__ == '__main__':
    args = _parse_args()
    find_clusters()
