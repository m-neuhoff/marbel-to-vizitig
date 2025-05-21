#!/bin/bash

#SBATCH --job-name=marbel               # Job name
#SBATCH --partition=bcf                # Partition name
#SBATCH --ntasks=1                      # Run on a single task
#SBATCH --cpus-per-task=10             # Number of CPU cores per task
#SBATCH --mem=15gb                     # Total memory limit
#SBATCH --time=1-00:00:00           

main_folder=$1

marbel --n-species 10 \
        --n-orthogroups 2000 \
        --library-size 100000 \
        --n-samples 3 3 \
        --seed 23 \
        --outdir $main_folder/simulated_reads
