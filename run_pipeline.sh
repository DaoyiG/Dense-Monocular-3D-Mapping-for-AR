#!/bin/bash

# run this script under the directory of monodepth2
# you may need to first put all the test images in a test_images folder under assets/
# you will get the depth output for monodepth presentation, o3d and infiniTAM

echo "===================================="
echo "Set up folders for specific outputs"
echo "===================================="

export dir=$PWD
#
mkdir $dir/assets/output_depth_rendering/
mkdir $dir/assets/output_depth_infinitam/
mkdir $dir/assets/output_npy_mono/
mkdir $dir/assets/output_depth_o3d/

## Rename the name of the image from 10-digits to 4
## Only need to run ONCE for a new dataset
#for file in ./assets/test_images/*
#do
#  lastfour=${file:23}
##  lastfour="${file:27:30}"
#  filename=${file:0:21}$lastfour
#  echo $filename
#
#  mv $file $filename
#done

echo "===================================="
echo "Render input rgb images to video"
echo "===================================="
python pic2video.py --image_path ./assets/test_images/ --output_name input.mp4
echo "===================================="
echo "See rendered video under current directory"
echo "===================================="
open input.mp4


echo "===================================="
echo "Depth Prediction Started"
echo "===================================="

for file in ./assets/test_images/*; do
  python test_simple.py --image_path $file --output_depth ./assets/output_depth_rendering/ --output_npy ./assets/output_npy_mono/ \
    --output_depth_o3d ./assets/output_depth_o3d/ --output_depth_infi ./assets/output_depth_infinitam/ \
    --model_name mono_1024x320 --no_cuda
done

echo "===================================="
echo "Depth Prediction Finished"
echo "===================================="


echo "===================================="
echo "Render output depth images to video"
echo "===================================="
python pic2video.py --image_path ./assets/output_depth_rendering/ --output_name depth.mp4
echo "===================================="
echo "See rendered video under current directory"
echo "===================================="
open depth.mp4


echo "===================================="
echo "Convert depth and rgb image to infinitam format"
echo "===================================="
cp -r $dir/assets/test_images/ $dir/assets/output_rgb_infinitam/

cd $dir/assets/output_rgb_infinitam/ && magick mogrify -format ppm *.png
cd $dir/assets/output_depth_infinitam/ && magick mogrify -format pgm *.png

echo "===================================="
echo "Done"
echo "===================================="

# move scene image and o3d depth to o3d reconstruction pipeline
cp -r $dir/assets/test_images/ $dir/o3d/ReconstructionSystem/dataset/kitti_2/image/
cp -r $dir/assets/output_depth_o3d/ $dir/o3d/ReconstructionSystem/dataset/kitti_2/depth/

sleep 1

echo "===================================="
echo "Start Reconstruction Using Open3d"
echo "===================================="

sleep 1

cd $dir/o3d/ReconstructionSystem/
python run_system.py $dir/o3d/ReconstructionSystem/config/kitti_2.json --make --register --refine --integrate

echo "===================================="
echo "Visualize Reconstruction"
echo "===================================="
cd $dir/src
python pcd_vis.py --scene_path $dir/o3d/ReconstructionSystem/dataset/kitti_2/scene/integrated.ply --ext ply

# run InfiniTAM
echo "===================================="
echo "Start Reconstruction Using InfiniTAM"
echo "===================================="


cd $HOME/Infinitam_kitti/InfiniTAM/build/Apps/InfiniTAM/
./InfiniTAM $HOME/Infinitam_kitti/InfiniTAM/kitti/calib3.txt \
  $dir/assets/output_rgb_infinitam/%04i.ppm \
  $dir/assets/output_depth_infinitam/%04i.pgm

echo "===================================="
echo "Reconstruction Finished"
echo "===================================="

echo "===================================="
echo "Visualize Reconstruction"
echo "===================================="
cd $dir/src
python pcd_vis.py --scene_path $HOME/kitti_1500_001vox.obj --ext obj

wait

echo "===================================="
echo "All Done"
echo "===================================="