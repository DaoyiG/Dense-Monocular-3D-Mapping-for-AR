# Reconstruction Using InfiniTAM v3

## Important  
We use a filebased tracker which can read gt poses and speed up the reconstruction phase. 
You need to modify the path to your pose files under  
```
ITMLLib/Utils/ITMLibSettings.cpp
```
# 1. Building the System

### 1.1 Requirements

Several 3rd party libraries are needed for compiling InfiniTAM. The given version numbers are checked and working, but different versions might be fine as well. Some of the libraries are optional, and skipping them will reduce functionality.

  - cmake (e.g. version 2.8.10.2 or 3.2.3)
    REQUIRED for Linux, unless you write your own build system
    OPTIONAL for MS Windows, if you use MSVC instead
    available at http://www.cmake.org/

  - OpenGL / GLUT (e.g. freeglut 2.8.0 or 3.0.0)
    REQUIRED for the visualisation
    the library should run without
    available at http://freeglut.sourceforge.net/

  - CUDA (e.g. version 6.0 or 7.0)
    OPTIONAL but REQUIRED for all GPU accelerated code
    at least with cmake it is still possible to compile the CPU part without
    available at https://developer.nvidia.com/cuda-downloads

  - OpenNI (e.g. version 2.2.0.33)
    OPTIONAL but REQUIRED to get live images from suitable hardware
    also make sure you have freenect/OpenNI2-FreenectDriver if you need it
    available at http://structure.io/openni

  - libpng (e.g. version 1.6)
    OPTIONAL, allows to read PNG input files
    available at http://libpng.org

  - FFMPEG (e.g. version 2.8.6)
    OPTIONAL, allows writing and playback of lossless FFV1 encoded videos
    available at https://www.ffmpeg.org/

  - librealsense (e.g. github version from 2016-MAR-22)
    OPTIONAL, allows to get live images from Intel Realsense cameras
    available at https://github.com/IntelRealSense/librealsense

  - librealsense2 (e.g. Intel® RealSense™ SDK 2.X)
    OPTIONAL, allows to get live images from Intel Realsense cameras
    available at https://github.com/IntelRealSense/librealsense

  - libuvc (e.g. github version from 2015-OCT-27)
    OPTIONAL, deprecated alternative to librealsense
    currently this works only with branch olafkaehler/master
    available at https://github.com/olafkaehler/libuvc

  - doxygen (e.g. version 1.8.2)
    OPTIONAL, builds a nice reference manual
    available at http://www.doxygen.org/

###1.2 Build Process

  To compile the system, use the standard cmake approach:
```
  $ mkdir build
  $ cd build
  $ cmake /path/to/InfiniTAM -DOPEN_NI_ROOT=/path/to/OpenNI2/
  $ make
```
  To create a doxygen documentation, just run doxygen:
```
  $ doxygen Doxyfile
```
  This will create a new directory doxygen-html/ containing all the
documentation.

### 1.3 Odds and Ends

Padding the data structure ITMVoxel in ITMLibDefines.h with one extra byte may or may not improve the overall performance on certain GPUs. On a NVidia GTX 680 it appears to do, on a GTX 780 it does not. Have a try yourself if you need the speed.

On Mac OS X 10.9 there are currently some issues with libc++ vs. libstdc++ in conjunction with CUDA. They eventually manifest in error messages like:
```
Undefined symbols for architecture x86_64: 
"std::ios_base::Init::Init()", referenced from:
      __GLOBAL__I_a in libITMLib.a(ITMLib_generated_ITMColorTracker_CUDA.cu.o)
      __GLOBAL__I_a in libITMLib.a(ITMLib_generated_ITMDepthTracker_CUDA.cu.o)
     [...]
```
In the current version of InfiniTAM these errors are avoided by specifying ```CMAKE_CXX_FLAGS=-stdlib=libstdc++``` whenever clang is detected as complier. However, future versions of CUDA might not require this anymore or even get confused and/or require ```CUDA_HOST_COMPILER=/usr/bin/clang``` instead.

If a version of GLUT other than freeglut is used, the InfiniTAM sample application has problems on exit, as it is currently not explicitly cleaning up CUDA memory or closing the OpenNI device. Use freeglut to avoid this if you experience any problems.

Some sensors may need a small change to work correctly with OpenNI, the changes are described [here](http://com.occipital.openni.s3.amazonaws.com/Structure%20Sensor%20OpenNI2%20Quick%20Start%20Guide.pdf).


# 2. Sample Programs

The build process should result in an executable InfiniTAM, which is the main sample program. For a version without visualisation, try InfiniTAM_cli. If compiled with OpenNI support, both should run out-of-the-box without problems for live reconstruction. If you have calibration information for your specific device, you can pass it as the first argument to the program, e.g.:
```
  $ ./InfiniTAM Teddy/calib.txt
```
If no OpenNI support has been compiled in, the program can be used for offline processing:
```
  $ ./InfiniTAM Teddy/calib.txt Teddy/Frames/%04i.ppm Teddy/Frames/%04i.pgm
```
The arguments are essentially masks for sprintf and the %04i will be replaced by a running number, accordingly.

