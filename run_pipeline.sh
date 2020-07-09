#!/bin/bash

# run this script under the directory of monodepth2
# you may need to first put all the test images in a test_images folder under assets/
# you will get the depth output for monodepth presentation, o3d and infinitam

mkdir ./assets/output_depth_mono/
mkdir ./assets/output_npy_mono/
mkdir ./assets/output_depth_o3d/
mkdir ./assets/output_depth_infinitam/

# Rename the name of the image from 10-digits to 4
# Only need to run ONCE for a new dataset
#for file in ./assets/test_images/*
#do
#  lastfour="${file:27:30}"
#  filename=${file:0:21}$lastfour
#  mv $file $filename
#done

echo "===================================="
echo "Depth Prediction Started"
echo "===================================="

for file in ./assets/test_images/*
do
  python test_simple.py --image_path $file --output_depth ./assets/output_depth_mono/ --output_npy ./assets/output_npy_mono/ --model_name mono_1024x320 --no_cuda
  python test_o3d.py --image_path $file --output_depth ./assets/output_depth_o3d/ --output_npy ./assets/output_npy_mono/ --model_name mono_1024x320 --no_cuda
  python test_infinitam.py --image_path $file --output_depth ./assets/output_depth_infinitam/ --output_npy ./assets/output_npy_mono/ --model_name mono_1024x320 --no_cuda
done

echo "===================================="
echo "Depth Prediction Finished"
echo "===================================="

echo "Start rendering the output depth image to video"
python dep2video.py
echo "See rendered video under current directory"
echo "===================================="

echo "Convert depth and rgb image to infinitam format"
cp -r ./assets/test_images/ ./assets/output_rgb_infinitam/
cd ./assets/output_rgb_infinitam/ && magick mogrify -format ppm *.png
cd ../output_depth_infinitam/ && magick mogrify -format pgm *.png

# move scene image and o3d depth to o3d reconstruction pipeline
cd .. && cd ..
cp -r ./assets/test_images/ ./o3d/ReconstructionSystem/dataset/kitti_0/image/
cp -r ./assets/output_depth_o3d/ ./o3d/ReconstructionSystem/dataset/kitti_0/depth/

echo "===================================="
echo "Start Reconstruction Using Open3d"

cd ./o3d/ReconstructionSystem/ && python run_system.py ./config/kitti_0.json --make --register --refine --integrate


# run InfiniTAM
#echo "===================================="
#echo "Start Reconstruction Using InfiniTAM"
#cd .. && cd .. && cd InfiniTAM_kitti/build/App/InfiniTAM/
#./InfiniTAM [calib.txt] [rgb_path] [depth_path]


wait

echo "All done"
