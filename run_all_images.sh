#!/bin/bash

# run this script under the directory of monodepth2
# you may need to first put all the test images in a test_images folder under assets/
# run the test of monodepth2 function for all the image files in test_images folder

mkdir ./assets/output_depth/
mkdir ./assets/output_npy/
for file in ./assets/test_images/*
do
  python test_simple.py --image_path $file --output_depth ./assets/output_depth/ --output_npy ./assets/output_npy/ --model_name mono_1024x320 --no_cuda
done

wait

echo "All done"
