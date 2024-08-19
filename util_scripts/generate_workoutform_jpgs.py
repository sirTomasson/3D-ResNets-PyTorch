import subprocess
import argparse
import os
import json

from pathlib import Path
from .generate_video_jpgs import video_process


def generate_jpgs(labels_path, videos_path, dst_path):
    subsets = ['error_knees_forward.json', 'error_knees_inward.json']
    for subset in subsets:
        label_path = labels_path / subset
        assert os.path.exists(labels_path), f'{labels_path} does not exist'
        with open(label_path) as f:
            label_json = json.load(f)

        for key in label_json:
            video_path = videos_path / f'{key}.mp4'
            assert os.path.exists(video_path), f'{video_path} does not exist'
            video_process(video_path, dst_path, '.mp4')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'dir_path', default=None, type=Path, help='Directory path of videos')
    parser.add_argument(
        'dst_path',
        default=None,
        type=Path,
        help='Directory path of jpg videos')
    parser.add_argument(
        '--n_jobs', default=-1, type=int, help='Number of parallel jobs')
    parser.add_argument(
        '--fps',
        default=-1,
        type=int,
        help=('Frame rates of output videos. '
              '-1 means original frame rates.'))
    parser.add_argument(
        '--size', default=240, type=int, help='Frame size of output videos.')
    args = parser.parse_args()
    labels_path = args.dir_path / 'Labels'
    videos_path = args.dir_path / 'videos'
    generate_jpgs(labels_path, videos_path, args.dst_path)

