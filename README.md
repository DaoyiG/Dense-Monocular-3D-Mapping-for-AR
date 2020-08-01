# Dense-Monocular-3D-Mapping-for-AR
### Members:  
[HanzhiC](https://github.com/HanzhiC)  
[Spazierganger](https://github.com/Spazierganger)  
[DaoyiG](https://github.com/DaoyiG)

### Project Description:
This is the course project of **Perception and Learning in Robotics and Augmented Reality** in summer semester 2020 in computer vision group from TUM Chair for Computer Aided Medical Procedures & Augmented Reality.  

The pipeline of our project is from a sequence of monocular RGB images to a dense 3D reconstruction, and an automatic ( manual as well) AR pipeline to create a sequence of augmented images.  
### Project Environment:  
Create our environment with 
```
conda create -n rec4aug python=3.6.6
```

After activate the environment ```rec4aug```, you need to install:
```
conda install pytorch=0.4.1 torchvision=0.2.1 -c pytorch
pip install open3d
pip install opencv-python
```
### Run Whole Pipeline  
You can simply use terminal under this directory and type
```
bash run_pipeline.sh
```
to run the whole pipeline of our project. You can choose whether to skip a stage( e.g. reconstruction using open3d) 
by entering y or N with respect to corresponding shell prompt.
### Additional Dependencies:

We use imagemagick to transform the output of monodepth to the format taken by InfiniTAM  
[imagemagick](https://imagemagick.org/)

### Related Works:  
[Digging into Self-Supervised Monocular Depth Prediction (Monodepth2)](https://github.com/nianticlabs/monodepth2)  

[InfiniTAM v3](https://github.com/victorprad/InfiniTAM)  

[OpenSfM](https://github.com/mapillary/OpenSfM)  

[Open3d Reconstruction Pipeline](https://github.com/intel-isl/Open3D/tree/master/examples/python/ReconstructionSystem)  

[Augmented Reality Meets Computer Vision : Efficient Data Generation for Urban Driving Scenes](https://arxiv.org/abs/1708.01566)  


