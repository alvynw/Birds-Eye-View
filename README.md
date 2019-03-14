# System Requirements
All code supports Linux. The transformation algorithm will work on any OS, however, a number of features, namely persistant camera ports and run-on-start will not work. I am confident there are solutions for other OSs, however, the current code does not support OSs besides Linux.

### Making Camera Ports Persistant in Ubuntu

Because there are multiple cameras used in this project, and the relative position of every camera (to other cameras) is important, it is imperative we have a method ensuring the camera gets to the right location every time. Otherwise, you might, for example, get the top camera stream on the left and the left camera stream on the bottom, etc., which is undesireable. 

The method this project uses to ensure cameras are connected to the right port everytime is through symlinks. 
1. Create a file under `/etc/udev/rules.d` called `25-birds-eye.rules`.
2. To add make a camera port persistant, add the following line. Change the serial id, vendor id, and product id as neccessary. Change the symlink to a name that can easily identify the camera you are using. Do not use anything in the form of `video#` where `#` is a number
```
KERNEL=="video*", ATTRS{serial}=="F2814710", ATTRS{idVendor}=="046d", ATTRS{idProduct}=="081b", SYMLINK+="LOGITECH_C310_TOP"
```
3. To use the symlink, pass your symlink as a parameter to `connectCamera(symlink)`. For example, if you used the example above, you would do `connectCamera("LOGITECH_C310_TOP")`.

#### How this method works internally
The `rules` file creates a symlink `/dev/{NAME}` that links to the corresponding video capture id. `connectCamera(symlink)` follows this link to find the video capture id (`/dev/video{id}`) of the camera. The id is then passed into `VideoCapture(id)`. 


