# vslam_failures_rss23_safe_autonomy
Repository containing code and instructions for Visual SLAM failures assessment performed for the RSS 2023 Safe Autonomy Workshop Competition

# Links
- The failure analysis video can be found [here](https://www.youtube.com/watch?v=TVz5XrXm8Wo).
- The rosbags from SCAND that we used can be obtained from [here](https://www.cs.utexas.edu/~xiao/SCAND/SCAND.html). The specific names of the bags that we used have been provided in the SCAND_bags.txt file.
- The rosbags from IV-SLAM can be obtained from [here](https://drive.google.com/drive/folders/1S1-A3wXpdJCQVFmZmJFfIHJxKWl2OfuP?usp=drive_link). The link also contains the failure analysis results for both the IV-SLAM and SCAND bags.

# Basic Setup
- Clone this repository with the `--recursive` flag to pull all submodules too

# DROID-SLAM
## Setup:
- Create a conda environment using the `droidenv.yaml` file:
```
conda env create -f droidenv.yaml
```
- Activate the conda environment and run the following commands:
```
conda activate droidenv
pip install evo --upgrade --no-binary evo
pip install gdown
```
- Compile the extensions (takes about 10 minutes):
```
cd third_party/DROID-SLAM
python setup.py install
```
- Download the model from google drive: [droid.pth](https://drive.google.com/file/d/1PpqVt1H4maBa_GbPJp4NwxRsd9jk-elh/view?usp=sharing) and put it in DROID-SLAM folder
- Dump your data of interest in the KITTI format. It should look like this (for stereo data, else exclude image_1 folder):
```
sequence/
  ├── image_0/
  | ├── 000000.png
  | ├── 000001.png
  | ├── 000002.png
  | ├── ...
  ├── image_1/
  | ├── 000000.png
  | ├── 000001.png
  | ├── 000002.png
  | ├── ...
  ├── times.txt
``` 
The names of the images within image_0 and image_1 directories should match. For example, the first left image and first right image should both be named 000001.png, second image should be named 000002.png.
- Create a `.txt` calibration file for the camera intrinsics. An example is provided in the `calib` folder. The format is as follows where the parameters in the brackets are optional:
```
fx fy cx cy [k1 k2 p1 p2 [ k3 [ k4 k5 k6 ]]]
```

## Running with monocular data:
- Activate the conda environment if not already done and cd to the DROID-SLAM directory:
```
conda activate droidenv
cd third_party/DROID-SLAM
```
- Run DROID-SLAM
  - `python demo.py --imagedir <path to directory that contains ordered images> --calib <path to calibration file> --buffer <optional buffer size> --stride <optional stride>`
    -  The buffer is the maximum number of poses that can be estimated. If too large, global BA won’t have enough memory. We have used 850 for a GPU with 16 GB memory.
    -  The stride controls how many images are used. The default is 3, which means that every 3rd image will be used in trajectory evaluation. If the number of images is greater than the buffer size, the stride parameter must be set to scale the number of images used. 

## Running with stereo data:
- Update the stereo calibration in code:
  - Edit the variables in the block denoted here: https://github.com/ut-amrl/DROID-SLAM/blob/addStereo/demo.py#L63 
  - For appropriately configured ROS bags, these variables can mostly be obtained from the camera info topic
- Activate the conda environment if not already done and cd to the DROID-SLAM directory:
```
conda activate droidenv
cd third_party/DROID-SLAM
```
- Run DROID-SLAM
  - `python demo.py --imagedir <path to directory that contains ordered left images> --right_imagedir <path to directory that contains ordered right images> --calib <path to calibration file> --buffer <optional buffer size> --stride <optional stride>`
    -  The buffer is the maximum number of poses that can be estimated. If too large, global BA won’t have enough memory. We have used 850 for a GPU with 16 GB memory.
    -  The stride controls how many images are used. The default is 3, which means that every 3rd image will be used in trajectory evaluation. If the number of images is greater than the buffer size, the stride parameter must be set to scale the number of images used. 

# ORB-SLAM3 
## Setup:
- Follow the build instructions in the [README](https://github.com/ut-amrl/ORB_SLAM3).
- Alternatively, you can also use this docker image: tiejean/rss2023competition:orb_slam3
  - To run this docker with x display, you can use this repo. To use this repo directly, similar to how this directory is set up, you can create dummy Makefile and Dockerfile, and copy-paste the compose.yaml and modified the specified docker image you use.
  - Run bash build.sh && bash build_ros.sh
  - Known compilation errors: I’ve noticed that if you have conflicting opencv versions on your machine, you might encounter memory issue when rectifying images. On rss2023 branch, I asked cmake to find the exact version of opencv. If you don’t have the same version of opencv installed and you don’t want to use the docker image, you can use this script to preprocess all the input images and set the do_rectify flag to be false when running ORB_SLAM3
- Use the example settings file provided in the `calib` folder and modify the camera calibration parameters as needed

## Running with monocular data:
- `cd third_party/ORB_SLAM3/Examples/Monocular`
- Run `./mono_kitti path_to_vocabulary path_to_settings path_to_sequence` where:
  - `path_to_vocabulary` is the path to the ORBvoc.txt file in the Vocabulary folder
  - `path_to_settings` is the path to the settings file
  - `path_to_sequence` is the path to the sequence directory containing the image directories and times.txt file

## Running with stereo data:
- `cd third_party/ORB_SLAM3/Examples/Stereo`
- Run `./stereo_kitti path_to_vocabulary path_to_settings path_to_sequence <do_rectify> <start_frame_id> <end_frame_id>`
  - For example, to run the a whole bag:
    - On raw data: `./stereo_kitti ../../Vocabulary/ORBvoc.txt IVSLAM.yaml <path_to_raw_KITTI_images> true`
    - On rectified data: `./stereo_kitti ../../Vocabulary/ORBvoc.txt IVSLAM.yaml <path_to_rectified_KITTI_images> false`
    - To replicate failure on some segment: `./stereo_kitti ../../Vocabulary/ORBvoc.txt IVSLAM.yaml <path_to_raw_KITTI_images> true`
  - path_to_raw_KITTI_images expect a directory that contains “image_0”, “image_1” and “times.txt”
  - Currently, the trajectories are saved to Examples/Stereo/CameraTrajectory.txt. (I should’ve added a flag to specified the output trajectory path but I haven’t done so…) So you may need to manually move/rename the output trajectory file if you think you want to visualize those trajectories against groundtruth later

## Known issues with running ORB_SLAM3:
 - Sometimes the Sophus Library gives error saying got nan. Ignoring those error messages for this competition for now
 - Sometimes g2o reports 0 vertices to optimize. Ignoring those error messages as well

# LeGO-LOAM (for reference trajectory generation)
## Setup
- Follow the set up instructions [here](https://github.com/ut-amrl/LeGO-LOAM-1/tree/writeResultsWithTimestampsToFileVelodyne).
- Follow the instructions to run, replacing step 1 with `roslaunch lego_loam run.launch results_dir:=<directory for results>`
  - The results directory must exist and contain the subfolders `poses` and `point_clouds` before LeGO-LOAM is run

# TODO
- ~~Add links to datasets~~
- ~~Add links for rosbag to dataset format conversion~~
- ~~Add links for plotting scripts~~
- ~~Add link to video~~
- Change dataset link to one with public access
- Upload IV-SLAM bags to [drive](https://drive.google.com/drive/folders/1119aEdqI60oiO5oI7LpZ6aDjFGv-LiKa?usp=drive_link)
