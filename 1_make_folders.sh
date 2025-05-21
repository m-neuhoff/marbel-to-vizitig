#!/bin/bash
# start this script out of the repo's main folder

main_folder=$1

mkdir $main_folder
cd $main_folder
mkdir samples GA_transcripts graphs file_list_csv simulated_reads

cd ..