## Making Camera Ports Persistant in Ubuntu
The method used is symlinks.
1. Create a file under `/etc/udev/rules.d` called `25-birds-eye.rules`.
2. To add make a camera port persistant, add the following line. Change the serial id, vendor id, and product id as neccessary. Change the symlink to a name that can easily identify the camera you are using.
```
KERNEL=="video*", ATTRS{serial}=="F2814710", ATTRS{idVendor}=="046d", ATTRS{idProduct}=="081b", SYMLINK+="LOGITECH_C310_TOP"
```
3. To use the symlink, pass your symlink as a parameter to `connectCamera(symlink)`. For example, if you used the example above, you would do `connectCamera("LOGITECH_C310_TOP")`


