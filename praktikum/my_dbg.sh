#!/bin/bash

#SBATCH --job-name=dbg               # Job name
#SBATCH --partition=bcf                # Partition name
#SBATCH --ntasks=1                      # Run on a single task
#SBATCH --cpus-per-task=4             # Number of CPU cores per task
#SBATCH --mem=4gb                     # Total memory limit
#SBATCH --time=1-00:00:00           

PATH="/homes/mneuhoff/git_projekte/dbg/target/release:$PATH"

# go into folder with reads to execute
cd ~/git_projekte/marbel/simulated_reads/

# -r should be half of the job memory request
dbg --csv ~/git_projekte/marbel/simulated_reads/summary/samples.csv \
    --memory 2 \
    --out ~/git_projekte/graphs/my_test.gfa \
    --format gfa \