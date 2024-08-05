#!/bin/bash

in_dir=$1
out_dir=$2

# Ensure output directory exists
mkdir -p "$out_dir"

for video in "$in_dir"/*.mp4; do
    if [ -f "$video" ]; then
        filename=$(basename "$video")
        output_file="$out_dir$filename"
        echo "Processing $video ..."
        # Uncomment the following line to execute FFmpeg command
        ../ffmpeg/bin/ffmpeg.exe -i "$video" -c:v libx264 "$output_file"
        echo "Output file: $output_file"
    fi
done


