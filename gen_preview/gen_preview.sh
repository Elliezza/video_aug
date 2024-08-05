input_folder=$1
output_folder=$2

for video in $input_folder/*; do
	if [[ "$video" == *.mp4 ]]; then
		echo $video
		python gen_capture.py -f $video -o $output_folder
	fi
done
