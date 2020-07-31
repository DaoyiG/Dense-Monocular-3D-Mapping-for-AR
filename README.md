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
conda env create -f environment.yml
```

### Additional Dependencies:

We use imagemagick to transform the output of monodepth to the format taken by InfiniTAM  
[imagemagick](https://imagemagick.org/)

### Related Works:  
[Digging into Self-Supervised Monocular Depth Prediction (Monodepth2)](https://github.com/nianticlabs/monodepth2)  

[InfiniTAM v3](https://github.com/victorprad/InfiniTAM)  

[OpenSfM](https://github.com/mapillary/OpenSfM)  

[Open3d Reconstruction Pipeline](https://github.com/intel-isl/Open3D/tree/master/examples/python/ReconstructionSystem)  

[Augmented Reality Meets Computer Vision : Efficient Data Generation for Urban Driving Scenes](https://arxiv.org/abs/1708.01566)  


