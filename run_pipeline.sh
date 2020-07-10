#!/bin/bash

# run this script under the directory of monodepth2
# you may need to first put all the test images in a test_images folder under assets/
# you will get the depth output for monodepth presentation, o3d and infinitam

echo "===================================="
echo "Set up folders for specific outputs"
echo "===================================="

export dir=$PWD

mkdir $dir/assets/output_depth_mono/
mkdir $dir/assets/output_npy_mono/
mkdir $dir/assets/output_depth_o3d/
mkdir $dir/assets/output_depth_infinitam/

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

for file in ./assets/test_images/*; do
  python test_simple.py --image_path $file --output_depth ./assets/output_depth_mono/ --output_npy ./assets/output_npy_mono/ \
    --output_depth_o3d ./assets/output_depth_o3d/ --output_depth_infi ./assets/output_depth_infinitam/ \
    --model_name mono_1024x320 --no_cuda
done

echo "===================================="
echo "Depth Prediction Finished"
echo "===================================="

sleep 2

echo "===================================="
echo "Start rendering the output depth image to video"
python dep2video.py
echo "See rendered video under current directory"
echo "===================================="

sleep 2

echo "===================================="
echo "Convert depth and rgb image to infinitam format"
echo "===================================="
cp -r $dir/assets/test_images/ $dir/assets/output_rgb_infinitam/

cd $dir/assets/output_rgb_infinitam/ && magick mogrify -format ppm *.png
cd $dir/assets/output_depth_infinitam/ && magick mogrify -format pgm *.png

# move scene image and o3d depth to o3d reconstruction pipeline
cp -r $dir/assets/test_images/ $dir/o3d/ReconstructionSystem/dataset/kitti_0/image/
cp -r $dir/assets/output_depth_o3d/ $dir/o3d/ReconstructionSystem/dataset/kitti_0/depth/

sleep 2

echo "===================================="
echo "Start Reconstruction Using Open3d"
echo "===================================="

sleep 1

cd $dir/o3d/ReconstructionSystem/
python run_system.py $dir/o3d/ReconstructionSystem/config/kitti_0.json --make --register --refine --integrate

# run InfiniTAM
echo "===================================="
echo "Start Reconstruction Using InfiniTAM"
echo "===================================="

sleep 1

cd $HOME/Infinitam_kitti/InfiniTAM/build/Apps/InfiniTAM/
./InfiniTAM $HOME/Infinitam_kitti/InfiniTAM/kitti/calib6.txt \
  $dir/assets/output_rgb_infinitam/%04i.ppm \
  $dir/assets/output_depth_infinitam/%04i.pgm

echo "===================================="
echo "Reconstruction Finished"
echo "===================================="

wait

echo "All Done"
