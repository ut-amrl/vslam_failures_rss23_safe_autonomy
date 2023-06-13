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


# ORB-SLAM3 
## To set up ORB-SLAM3:
- Clone the AMRL fork of the orb_slam3 repo: 
  - https://github.com/ut-amrl/ORB_SLAM3
  - Checkout branch “rss2023”
- Follow the installation instructions in the README
  - Alternatively, you can also use this docker image: tiejean/rss2023competition:orb_slam3
- To run this docker with x display, you can use this repo. To use this repo directly, similar to how this directory is set up, you can create dummy Makefile and Dockerfile, and copy-paste the compose.yaml and modified the specified docker image you use.
- Run bash build.sh && bash build_ros.sh
- Known compilation errors: I’ve noticed that if you have conflicting opencv versions on your machine, you might encounter memory issue when rectifying images. On rss2023 branch, I asked cmake to find the exact version of opencv. If you don’t have the same version of opencv installed and you don’t want to use the docker image, you can use this script to preprocess all the input images and set the do_rectify flag to be false when running ORB_SLAM3

## To run ORB-SLAM with stereo KITTI data:
- cd Examples/Stereo
- Usage: `./stereo_kitti path_to_vocabulary path_to_settings path_to_sequence <do_rectify> <start_frame_id> <end_frame_id>`
  - For example, to run the a whole bag:
    - On raw data: `./stereo_kitti ../../Vocabulary/ORBvoc.txt IVSLAM.yaml <path_to_raw_KITTI_images> true`
    - On rectified data: `./stereo_kitti ../../Vocabulary/ORBvoc.txt IVSLAM.yaml <path_to_rectified_KITTI_images> false`
    - To replicate failure on some segment: `./stereo_kitti ../../Vocabulary/ORBvoc.txt IVSLAM.yaml <path_to_raw_KITTI_images> true`
  - path_to_raw_KITTI_images expect a directory that contains “image_0”, “image_1” and “times.txt”
  - Currently, the trajectories are saved to Examples/Stereo/CameraTrajectory.txt. (I should’ve added a flag to specified the output trajectory path but I haven’t done so…) So you may need to manually move/rename the output trajectory file if you think you want to visualize those trajectories against groundtruth later

## To run ORB-SLAM with monocular data:
 - cd Examples/Monocular
 - Usage: `./mono_kitti path_to_vocabulary path_to_settings path_to_sequence`
- path_to_sequence expect a directory that contains “image_0”, “image_1” and “times.txt”

## Known issues with ORB_SLAM3:
 - Sometimes the Sophus Library gives error saying got nan. Ignoring those error messages for this competition for now
 - Sometimes g2o reports 0 vertices to optimize. Ignoring those error messages as well



# TODO
- Add links or submodules to LeGO-LOAM
- Add instructions for running each
- Add links to datasets
- Add links for rosbag to dataset format conversion
- Add links for plotting scripts
- Add link to video
