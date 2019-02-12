import cv2 as cv
from image_stream import ImageStream
import subprocess
import time
import re
import numpy as np

ROBOT_WIDTH = 176
ROBOT_HEIGHT = 176
IMG_COLS = 256
IMG_ROWS = 192

SMALL_TRAPEZOID_LENGTH = 150

#transformation
#80 deg
src = np.float32([[170 // 2.5, 480 // 2.5], [207 // 2.5, 301 // 2.5], [436 // 2.5, 301 // 2.5], [473 // 2.5, 480 // 2.5]])
dst = np.float32([[430 // 5, 960 // 5], [430 // 5, 540 // 5], [850 // 5, 540 // 5], [850 // 5, 960 // 5]])

devices = ["LOGITECH_C310_TOP", "LOGITECH_C310_LEFT", "LOGITECH_C310_RIGHT", "LOGITECH_C310_BOT"]
devices_config = [["TOP", 0, 0, -ROBOT_HEIGHT // 2], ["LEFT", 90, -ROBOT_WIDTH // 2, 0], ["RIGHT", -90, ROBOT_WIDTH // 2, 0], ["BOT", 180, 0, +ROBOT_HEIGHT // 2]]

def connectCamera(device):
    cmd = "readlink -f /dev/%s" % (device)
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    # output of form /dev/videoX
    time.sleep(0.1)
    t = process.poll()
    if (t is not None):
        out = process.communicate()[0]
        pattern = "^/dev/video(\d+)"
        if (re.match(pattern, out)):
            video_id = int(re.search(pattern, out).group(1))
            print video_id
            
            return [True, video_id]
        else:
            print "%s not found1" % (device)
    else:
        print "%s not found2" % (device)

    try:
        process.terminate()
    except Exception:
        pass
    return [False, -1]

images = []



for index, device in enumerate(devices):

    ###linux
    ret, camera_id = connectCamera(device)
    if ret:
        config = devices_config[index]
        cam = cv.VideoCapture(camera_id)
        cam.set(cv.cv.CV_CAP_PROP_FPS, 60)
        cam.set(cv.cv.CV_CAP_PROP_FRAME_WIDTH, IMG_COLS )
	      cam.set(cv.cv.CV_CAP_PROP_FRAME_HEIGHT, IMG_ROWS)
	      cam.set(cv.cv.CV_CAP_PROP_FOURCC, cv.cv.CV_FOURCC('M', 'J', 'P', 'G'))
        images.append(ImageStream(config[0], cam, config[1], config[2], config[3]))
        
    ###mac
    #config = devices_config[index]
    #cam = cv.VideoCapture(1)
    #images.append(ImageStream(config[0], cam, config[1], config[2], config[3]))
