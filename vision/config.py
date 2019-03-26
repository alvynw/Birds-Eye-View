import cv2 as cv
from image_stream import ImageStream
import subprocess
import time
import re
import numpy as np
import glob

counter = 0

factor = 4

ROBOT_WIDTH = 700 // factor
ROBOT_HEIGHT = 700 // factor
IMG_COLS = 2560 // factor
IMG_ROWS = 1920 // factor

# transformation
# 85 deg

#2560x1920
transformation_src = np.float32([[300, 1920], [918, 1051], [1674, 1058], [2260, 1920]]) // factor

#almost full
transformation_dst = np.float32([[980, 1920], [980, 367], [1580, 367], [1580, 1920]]) // factor

# 80Deg
#
# [66,1920], [922, 673], [1710, 673], [2508, 1920]
#
# 60deg
#
# [478, 1920], [903, 253], [1639, 253], [2035, 1920]

#devices = ["LOGITECH_C310_TOP", "LOGITECH_C310_LEFT", "LOGITECH_C310_BOT", "LOGITECH_C310_RIGHT"]
#devices = ["LOGITECH_C310_TOP"]
device_configs = {
        "LOGITECH_C310_TOP":[0, 0, -ROBOT_HEIGHT // 2], 
        "LOGITECH_C310_LEFT":[90, -ROBOT_WIDTH // 2, 0], 
        "LOGITECH_C310_BOT":[180, 0, ROBOT_HEIGHT // 2], 
        "LOGITECH_C310_RIGHT":[-90, ROBOT_WIDTH // 2, 0]
}

devices = {
        "LOGITECH_C310_TOP":None, 
        "LOGITECH_C310_LEFT":None, 
        "LOGITECH_C310_BOT":None, 
        "LOGITECH_C310_RIGHT":None
}




def connectCamera(device):
    cmd = "readlink -f /dev/%s" % (device)
    try:
        out = subprocess.check_output(cmd.split())
        pattern = "^/dev/video(\d+)"
        if (re.match(pattern, out)):
            video_id = int(re.search(pattern, out).group(1))
            # print video_id

            return [True, video_id]
        raise Exception
    except:
        print "%s not found" % (device)
        return [False, -1]

def setUpDevice(device, camera_id):
	config = device_configs[device]
	cam = cv.VideoCapture(camera_id)
	cam.set(cv.cv.CV_CAP_PROP_FPS, 10)
	cam.set(cv.cv.CV_CAP_PROP_FRAME_WIDTH, 160)
	cam.set(cv.cv.CV_CAP_PROP_FRAME_HEIGHT, 120)
	print cam.get(cv.cv.CV_CAP_PROP_FRAME_WIDTH)
	print cam.get(cv.cv.CV_CAP_PROP_FRAME_HEIGHT)
	devices[device] = ImageStream(device, cam, config[0], config[1], config[2])
	images.append(device)

images = []

for device in devices.keys():
    ''''''
    ###linux
    ret, camera_id = connectCamera(device)
    if ret:
    	 setUpDevice(device, camera_id)
         


###mac
#config = devices_config[0]
#cam = cv.VideoCapture(0)
#images.append(ImageStream(config[0], cam, config[1], config[2], config[3]))

#config = devices_config[1]
#cam = cv.VideoCapture(1)
#images.append(ImageStream(config[0], cam, config[1], config[2], config[3]))
#config = devices_config[2]
#cam = cv.VideoCapture(2)
#images.append(ImageStream(config[0], cam, config[1], config[2], config[3]))
#config = devices_config[3]
#cam = cv.VideoCapture(3)
#images.append(ImageStream(config[0], cam, config[1], config[2], config[3]))

counter = len(glob.glob("/dev/video*"))

for img in images:
    print img
    t = time.time()
    devices[img].camera.read()
    print time.time() - t
