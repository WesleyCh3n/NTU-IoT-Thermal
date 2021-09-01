# NTU-IoT-Thermal

[![WesleyCh3n - NTU-IoT-Thermal](https://img.shields.io/badge/WesleyCh3n-NTU--IoT--Thermal-2ea44f?logo=github)](https://github.com/WesleyCh3n/NTU-IoT-Thermal)
![Python - >=3.7.3](https://img.shields.io/badge/Python->=3.7.3-informational?logo=Python) 
![OpenCV - 4.4.0.46](https://img.shields.io/badge/OpenCV-4.4.0.46-informational?logo=OpenCV)
[![hackmd-github-sync-badge](https://hackmd.io/Ssdg5RdgT7qWq_nrwQcSHA/badge)](https://hackmd.io/Ssdg5RdgT7qWq_nrwQcSHA)

This is NTU BME MS thesis project which using Pi Camera and FLIR Lepton 3.5 capture RGB and thermal image. Then post-processing both image to get the cow eyes temperature.

## Screenshot

![](https://i.imgur.com/gidqbM4.png)

## Required Package
- opencv-contrib-python
    ```bash
    sudo apt install libaec0 libaom0 libatk-bridge2.0-0 libatk1.0-0 libatlas3-base libatspi2.0-0 libavcodec58 libavformat58 libavutil56 libbluray2 libcairo-gobject2 libcairo2 libchromaprint1 libcodec2-0.8.1 libcroco3 libdatrie1 libdrm2 libepoxy0 libfontconfig1 libgdk-pixbuf2.0-0 libgfortran5 libgme0 libgraphite2-3 libgsm1 libgtk-3-0 libharfbuzz0b libhdf5-103 libilmbase23 libjbig0 libmp3lame0 libmpg123-0 libogg0 libopenexr23 libopenjp2-7 libopenmpt0 libopus0 libpango-1.0-0 libpangocairo-1.0-0 libpangoft2-1.0-0 libpixman-1-0 librsvg2-2 libshine3 libsnappy1v5 libsoxr0 libspeex1 libssh-gcrypt-4 libswresample3 libswscale5 libsz2 libthai0 libtheora0 libtiff5 libtwolame0 libva-drm2 libva-x11-2 libva2 libvdpau1 libvorbis0a libvorbisenc2 libvorbisfile3 libvpx5 libwavpack1 libwayland-client0 libwayland-cursor0 libwayland-egl1 libwebp6 libwebpmux3 libx264-155 libx265-165 libxcb-render0 libxcb-shm0 libxcomposite1 libxcursor1 libxdamage1 libxfixes3 libxi6 libxinerama1 libxkbcommon0 libxrandr2 libxrender1 libxvidcore4 libzvbi0
    pip3 install opencv-contrib-python
    ```
- libusb
    ```bash
    sudo apt-get install cmake libusb-1.0-0-dev -y
    git clone https://github.com/groupgets/libuvc
    cd libuvc 
    mkdir build && cd build
    cmake ..
    make && sudo make install
    sudo ldconfig -v
    sudo sh -c "echo 'SUBSYSTEMS==\"usb\", ATTRS{idVendor}==\"1e4e\", ATTRS{idProduct}==\"0100\", SYMLINK+=\"pt1\", GROUP=\"usb\", MODE=\"666\"' > /etc/udev/rules.d/99-pt1.rules"
    ```

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