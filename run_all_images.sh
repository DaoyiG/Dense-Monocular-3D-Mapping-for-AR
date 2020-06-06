#!/bin/bash

# run this script under the directory of monodepth2
# you may need to first put all the test images in a data_samples folder under assets/
# run the test of monodepth2 function for all the image files in data_dir

mkdir ./assets/output/
for file in ./assets/data_samples/*
do
  python test_simple.py --image_path $file --output_path ./assets/output/ --model_name mono_1024x320 --no_cuda
done

wait

echo "All done"
