import argparse

import numpy as np

from PIL import Image
from glob import glob
from os import path
from tqdm import tqdm
from joblib import Parallel, delayed

import json


def process_images(image_paths):
    images = []
    for image_path in image_paths:
        image = np.array(Image.open(image_path).resize((240, 240)))
        images.append(image)
    
    images = np.stack(images) / 255.
    mean = np.mean(images, axis=(0, 1, 2))
    std = np.std(images, axis=(0, 1, 2))
    return mean, std



def calculate_dataset_mean(dataset_path):
    paths = glob(path.join(dataset_path, '**', '*.jpg'))
    batch_size = 100
    data_batches = [paths[i:i + batch_size] for i in range(0, len(paths), batch_size)]
    results = Parallel(n_jobs=72)(delayed(process_images)(batch) for batch in data_batches)
    
    means, stds = zip(*results)
    means = np.stack(means)
    stds = np.stack(stds)
    print(stds)
    print(stds.shape)
    overall_mean = np.mean(means, axis=0)
    overall_std = np.sqrt(np.mean([s**2 for s in stds], axis=0))
    print(f'mean: {overall_mean}')
    print(f'std: {overall_std}')

    with open('workoutform_mean.json', 'w') as f:
        json.dump({ 'std' : overall_std.tolist(), 'mean': overall_mean.tolist() }, f, indent=4)


if __name__ == '__main__':
      parser = argparse.ArgumentParser()
      parser.add_argument('data_path',
                          default=None,
                          type=str,
                          help='Directory path of workoutform dataset')

      args = parser.parse_args()

      calculate_dataset_mean(args.data_path)