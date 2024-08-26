import subprocess
import argparse
import os
import json

from pathlib import Path
from .utils import get_n_frames


def load_json(path):
    assert os.path.exists(path), f'{path} does not exist'
    with open(path) as f:
        return json.load(f)


def get_subset_label(key, train, val, test):
    if key in train:
        return 'training'
    elif key in val:
        return 'validation'
    else:
        return 'testing'


def get_label(key, kie, kfe):
    if len(kie[key]) > 0:
        return 'kie'
    elif len(kfe[key]) > 0:
        return 'kfe'
    else:
        return 'correct'


def convert_workoutform_json_to_json(dir_path, video_path, dst_json_path):
    labels_path = dir_path / 'Labels'
    splits_path = dir_path / 'Splits'
    kie_json = load_json(labels_path / 'error_knees_inward.json')
    kfe_json = load_json(labels_path / 'error_knees_forward.json')
    train_json = load_json(splits_path / 'train_keys.json')
    val_json = load_json(splits_path / 'val_keys.json')
    test_json = load_json(splits_path / 'test_keys.json')
    database = {
        'labels': ['kie', 'kfe', 'correct'],
        'database': {}
    }
    for video_dir in video_path.iterdir():
        database['database'][video_dir.name] = {}
        database['database'][video_dir.name]['subset'] = get_subset_label(video_dir.name,
                                                                          train_json,
                                                                          val_json,
                                                                          test_json)

        annotations = {}
        annotations['label'] = get_label(video_dir.name, kie_json, kfe_json)
        annotations['segment'] = (1, get_n_frames(video_dir) + 1)
        database['database'][video_dir.name]['annotations'] = annotations

    with open(dst_json_path, 'w') as f:
        json.dump(database, f, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dir_path',
                        default=None,
                        type=Path,
                        help='Directory path of workoutform dataset')
    parser.add_argument('video_path',
                        default=None,
                        type=Path,
                        help=('Path of video directory (jpg).'
                              'Using to get n_frames of each video.'))
    parser.add_argument('dst_dir_path',
                        default=None,
                        type=Path,
                        help='Directory path of dst json file.')

    args = parser.parse_args()

    dst_json_path = args.dst_dir_path / 'workoutform.json'
    convert_workoutform_json_to_json(args.dir_path, args.video_path, dst_json_path)
