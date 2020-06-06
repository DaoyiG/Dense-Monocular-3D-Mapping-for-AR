#!/bin/bash

# run this script under the directory of monodepth2
# you may need to first put all the test images in a data_samples folder under assets/
# run the test of monodepth2 function for all the image files in data_dir

mkdir ./assets/output/
for file in ./assets/data_samples/*
do
  python test_simple.py --image_path $file --model_name mono_1024x320 --no_cuda

done

echo "move the output image to the output folder under assets/"
mv assets/data_samples/*.jpeg assets/output/

echo "rename the jpeg files to png files"
cd assets/output
rename "s/_disp.jpeg/.png/" *

wait

echo "All done"
