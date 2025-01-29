#!/bin/bash

set -e  # Exit on any error

# COMMAND TO RUN:
# ./run6.sh > run6.log 2>&1 &


# ------------------------------------------------------------------------------
# CONFIGURATIONS
# ------------------------------------------------------------------------------

models=("convs2s")
datasets=("imdb" "gith" "dblp" "uspt")
gpus="6,7"

# ------------------------------------------------------------------------------
# END CONFIGURATIONS
# ------------------------------------------------------------------------------

declare -A dataset_paths
dataset_paths["toy_dblp"]="../data/preprocessed/dblp/toy.dblp.v12.json"
dataset_paths["dblp"]="../data/preprocessed/dblp/dblp.v12.json.filtered.mt75.ts3"
dataset_paths["gith"]="../data/preprocessed/gith/gith.data.csv.filtered.mt75.ts3"
dataset_paths["imdb"]="../data/preprocessed/imdb/imdb.title.basics.tsv.filtered.mt75.ts3"
dataset_paths["uspt"]="../data/preprocessed/uspt/uspt.patent.tsv.filtered.mt75.ts3"

script_name=$(basename "$0" .sh)

# Log file for all run times
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
times_dir="${SCRIPT_DIR}/../run_times"
logs_dir="${SCRIPT_DIR}/../run_logs"

# Ensure the directories exist
mkdir -p ../run_logs

cd ../src

# loop over models and each model over datasets
for model in "${models[@]}"; do
  for dataset in "${!datasets[@]}"; do

    current_dataset="${datasets[$dataset]}"
    current_dataset_path="${dataset_paths[$current_dataset]}"
    current_model="${current_dataset}_${model}"

    echo "Script: ${script_name}."
    echo ""
    # Get the start time
    start_time=$(date +%s)
    
    # Run the command with nohup and capture its PID
    nohup python3 -u main.py \
      -data $current_dataset_path \
      -domain $current_dataset \
      -model "nmt_${current_model}" \
      -gpus $gpus \
      > "../run_logs/${current_model}.log" 2> "../run_logs/${current_model}_errors.log" &
    
    pid=$!
    
    echo "Started process $pid for model: ${current_model} on dataset: ${current_dataset}."
    echo ""
    
    # Wait for the process to complete
    wait $pid
    
    # Get the end time
    end_time=$(date +%s)
    
    # Calculate the elapsed time in seconds
    elapsed_time=$(($end_time - $start_time))
    
    # Convert elapsed time into hours, minutes, and seconds
    hours=$(($elapsed_time / 3600))
    minutes=$(($elapsed_time % 3600 / 60))
    seconds=$(($elapsed_time % 60))
    
    # Format the elapsed time as Xh Xm Xs
    formatted_time="${hours}h ${minutes}m ${seconds}s"
    
    in_minutes=$(($elapsed_time / 60))
    
    echo "Process completed for model: ${current_model} on dataset: ${current_dataset}."
    echo "Elapsed time: ${formatted_time} ($in_minutes mins)."
    echo ""
  done
done