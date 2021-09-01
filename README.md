# NTU-IoT-Thermal

[![WesleyCh3n - NTU-IoT-Thermal](https://img.shields.io/badge/WesleyCh3n-NTU--IoT--Thermal-2ea44f?logo=github)](https://github.com/WesleyCh3n/NTU-IoT-Thermal)
![Python - >=3.7.3](https://img.shields.io/badge/Python->=3.7.3-informational?logo=Python) 
![OpenCV - 4.4.0.46](https://img.shields.io/badge/OpenCV-4.4.0.46-informational?logo=OpenCV)
[![hackmd-github-sync-badge](https://hackmd.io/Ssdg5RdgT7qWq_nrwQcSHA/badge)](https://hackmd.io/Ssdg5RdgT7qWq_nrwQcSHA)

This is NTU BME MS thesis project which using Pi Camera and FLIR Lepton 3.5 capture RGB and thermal image. Then post-processing both image to get the cow eyes temperature.

## Usage

### Capture RGB Image

```bash
python3 pi_cam.py [-h] [-s] [-v]
```

| Args | Info                                                       |
|:----:|:---------------------------------------------------------- |
|  -s  | save image per second in `rgb_img/%Y_%m_%d/` for 5:10 mins |
|  -v  | show image in windows                                      |
|  -h  | print help message                                         |

### Capture Thermal data

```bash
python3 pi_uvc_flir.py [-h] [-s] [-v]
```

| Args | Info                                                      |
|:----:|:--------------------------------------------------------- |
|  -s  | save thermal data in `IR_HDF5_*.HDF5` (9 fps)  for 5 mins |
|  -v  | show thermal image in windows                             |
|  -h  | print help message                                        |

### Backup data

```bash
./rsync_data.sh
```

### (Optional) Add to crontab

```bash
crontab -e
```

Then add something like below, you can choose whatever time you want.

```bash
30 11 * * * cd /path/to/code_dir/ && python3 pi_cam.py -s
30 11 * * * cd /path/to/code_dir/ && python3 pi_uvc_flir.py -s
40 11 * * * cd /path/to/code_dir/ && ./rsync_data.sh
```