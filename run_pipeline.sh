#!/bin/bash

# run this script under the directory of monodepth2
# you may need to first put all the test images in a test_images folder under assets/
# you will get the depth output for monodepth presentation, o3d and infinitam

mkdir ./assets/output_depth_mono/
mkdir ./assets/output_npy_mono/
mkdir ./assets/output_depth_o3d/
mkdir ./assets/output_npy_o3d/
mkdir ./assets/output_depth_infinitam/
mkdir ./assets/output_rgb_infinitam/

for file in ./assets/test_images/*
do
  python test_simple.py --image_path $file --output_depth ./assets/output_depth_mono/ --output_npy ./assets/output_npy_mono/ --model_name mono_1024x320 --no_cuda
  python test_o3d.py --image_path $file --output_depth ./assets/output_depth_o3d/ --output_npy ./assets/output_npy_o3d/ --model_name mono_1024x320 --no_cuda --is_o3d 1
done

wait

echo "All done"
