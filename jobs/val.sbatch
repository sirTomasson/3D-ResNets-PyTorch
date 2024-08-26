#!/bin/bash
# parameters for slurm
#SBATCH -c 8                       # number of cores, 1
#SBATCH --gres=gpu:ampere:1
#SBATCH --mail-type=END,FAIL          # email status changes (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --time=2:00:00                # time limit 1h

# show actual node in output file, useful for diagnostics
hostname

# Load all required software modules, including Python
module load nvidia/cuda-11.8
module load python/3.10.7   # Load the desired Python module, version might vary

# It's nice to have some information logged for debugging
echo "Gpu devices                 : "$CUDA_VISIBLE_DEVICES
echo "Starting worker: "

export HTTP_PROXY=http://proxy.utwente.nl:3128
export HTTPS_PROXY=http://proxy.utwente.nl:3128

# Run the Python script
python3 main.py --root_path ./data --video_path hmdb51_videos/jpgs --annotation_path hmdb51_1.json \
--result_path results --dataset hmdb51 --resume_path results/hmdb51/run6/save_175.pth \
--model_depth 101 --n_classes 51 --n_threads 4 --no_train --no_val --inference --output_topk 5 --inference_batch_size 1