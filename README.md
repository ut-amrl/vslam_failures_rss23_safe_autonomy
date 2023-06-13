# vslam_failures_rss23_safe_autonomy
Repository containing code and instructions for Visual SLAM failures assessment performed for the RSS 2023 Safe Autonomy Workshop Competition

# DROID-SLAM
## To set up droid-slam:
- Clone the AMRL fork of the droid-slam repo
https://github.com/ut-amrl/DROID-SLAM/tree/addStereo
- Set up the conda environment
  - Follow the instructions in the README
    - In the first command under step 2 of Getting started, I got stuck in ‘Solving environment’. If you run into those issues, you may want to start with my conda environment (replace environment.yaml in conda setup instructions with amanda_environment.yaml)
- Download the model (step 1 under demos)

## To run DROID-SLAM with monocular data:
- Dump your data of interest to KITTI format
  - i.e. make a directory with the images. The order in DROID-SLAM is determined by sorting the file names, so the recommended method is to pad the image names with leading zeros to ensure that they’re sorted appropriately. Ex. First image is named 00001.png and 10th image is 00010.png)
- Create a calibration file
  - See “Running on your own data” section of DROID-SLAM README
- Activate the droid-slam conda environment if not already done
  - `conda activate <environment name>`
- Run DROID-SLAM
  - `python demo.py --imagedir=<directory that contains ordered images> --calib=<calibration file> --buffer <optional buffer size> --stride <optional stride>`
    -  The buffer is the maximum number of poses that can be estimated. If too large, global BA won’t have enough memory. We have used 850 for a GPU with 16 GB memory.
    -  The stride controls how many images are used. The default is 3, which means that every 3rd image will be used in trajectory evaluation. If the number of images is greater than the buffer size, the stride parameter must be set to scale the number of images used. 

## To run DROID-SLAM with stereo data:
- Dump your data of interest to KITTI format
  - I.e. Make a directory for both the right and left cameras in the stereo pair. Suggested method is to make a directory that contains two directories: image_0, which contains the left images, and image_1, which contains the right images
  - The names of the images within their respective directories should match. For example, the first left image and first right image should both be named 00001.png, second image should be named 00002.png.
  - (As with monocular) The order in DROID-SLAM is determined by sorting the file names, so the recommended method is to pad the image names with leading zeros to ensure that they’re sorted appropriately. Ex. First image is named 00001.png and 10th image is 00010.png)
- Update the stereo calibration in code:
  - Edit the variables in the block denoted here: https://github.com/ut-amrl/DROID-SLAM/blob/addStereo/demo.py#L63 
  - For appropriately configured ROS bags, these variables can mostly be obtained from the camera info topic
- Activate the droid-slam conda environment if not already done
  - `conda activate <environment name>`
- Run DROID-SLAM
  - `python demo.py --imagedir=<directory that contains ordered images> --calib=<calibration file> --buffer <optional buffer size> --stride <optional stride>`
    -  The buffer is the maximum number of poses that can be estimated. If too large, global BA won’t have enough memory. We have used 850 for a GPU with 16 GB memory.
    -  The stride controls how many images are used. The default is 3, which means that every 3rd image will be used in trajectory evaluation. If the number of images is greater than the buffer size, the stride parameter must be set to scale the number of images used. 




# TODO
- Add links or submodules to LeGO-LOAM, our DROID-SLAM fork, and our ORB-SLAM3 fork. 
- Add instructions for running each
- Add links to datasets
- Add links for rosbag to dataset format conversion
- Add links for plotting scripts
- Add link to video
