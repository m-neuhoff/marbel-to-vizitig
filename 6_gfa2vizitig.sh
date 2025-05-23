#!/bin/bash

#SBATCH --job-name=converter               # Job name
#SBATCH --partition=bcf                # Partition name
#SBATCH --ntasks=1                      # Run on a single task
#SBATCH --cpus-per-task=1             # Number of CPU cores per task
#SBATCH --mem=1gb                     # Total memory limit
#SBATCH --time=1-00:00:00

# starten aus gfa-to-bcalm

main_folder=$1

python scripts/gfa2vizitig.py $main_folder/graphs/$main_folder'.gfa' $main_folder/graphs/$main_folder'.fa' 3 --sample_dir samples $main_folder/GA_transcripts/generated_transcripts.fa $main_folder/graphs/$main_folder'_aligned.gaf'