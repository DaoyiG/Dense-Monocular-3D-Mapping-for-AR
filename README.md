# Dense-Monocular-3D-Mapping-for-AR

### :student: Members:  
[HanzhiC](https://github.com/HanzhiC)  
[Spazierganger](https://github.com/Spazierganger)  
[DaoyiG](https://github.com/DaoyiG)

### :page_with_curl: Project Description:
This is the course project of **Perception and Learning in Robotics and Augmented Reality** in summer semester 2020 in computer vision group from TUM Chair for Computer Aided Medical Procedures & Augmented Reality.  

The pipeline of our project is from a sequence of monocular RGB images to a dense 3D reconstruction, and an automatic ( manual as well) AR pipeline to create a sequence of augmented images.  

<div align=center><img width="800" height="400" src="https://github.com/DaoyiG/Dense-Monocular-3D-Mapping-for-AR/blob/master/images/stages.png"/></div>  

>**1. Depth Prediction**  
<div align=center><img src="https://github.com/DaoyiG/Dense-Monocular-3D-Mapping-for-AR/blob/master/images/input%2000_00_00-00_00_30.gif"/></div>  
<div align=center><img src="https://github.com/DaoyiG/Dense-Monocular-3D-Mapping-for-AR/blob/master/images/depth%2000_00_00-00_00_30.gif"/></div>  

>**2. Reconstruction**
<div align=center><img src="https://github.com/DaoyiG/Dense-Monocular-3D-Mapping-for-AR/blob/master/images/blender1500_final%2000_00_00-00_00_30.gif"/></div>  

>**3. Augmentation**  
>>Auto Mode:  
<div align=center><img src="https://github.com/DaoyiG/Dense-Monocular-3D-Mapping-for-AR/blob/master/images/scene6%2000_00_00-00_00_30.gif"/></div>  

>>Manual Mode:  
<div align=center><img src="https://github.com/DaoyiG/Dense-Monocular-3D-Mapping-for-AR/blob/master/images/scene3_aug.png"/></div>  

### :gear: Project Environment:  
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
### :toolbox: Additional Dependencies:

We use imagemagick to transform the output of monodepth to the format taken by InfiniTAM  
[imagemagick](https://imagemagick.org/)  

### :clapper: Run Whole Pipeline  
You can simply use terminal under this directory and type
```
bash run_pipeline.sh
```
to run the whole pipeline of our project. You can choose whether to skip a stage( e.g. reconstruction using open3d) 
by entering y or N with respect to corresponding shell prompt.


### :link: Related Works:  
[Monodepth2](https://github.com/nianticlabs/monodepth2)  

[InfiniTAM v3](https://github.com/victorprad/InfiniTAM)  

[Open3d Reconstruction Pipeline](https://github.com/intel-isl/Open3D/tree/master/examples/python/ReconstructionSystem)  


