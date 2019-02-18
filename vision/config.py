import cv2 as cv
from image_stream import ImageStream
import subprocess
import time
import re
import numpy as np

ROBOT_WIDTH = 233
ROBOT_HEIGHT = 175
IMG_COLS = 320
IMG_ROWS = 240

# transformation
# 80 deg
transformation_src = np.float32([[170 // 2.5, 480 // 2.5], [207 // 2.5, 301 // 2.5], [436 // 2.5, 301 // 2.5], [473 // 2.5, 480 // 2.5]])
transformation_dst = np.float32([[430 // 5, 960 // 5], [430 // 5, 540 // 5], [850 // 5, 540 // 5], [850 // 5, 960 // 5]])

devices = ["LOGITECH_C310_TOP", "LOGITECH_C310_LEFT", "LOGITECH_C310_BOT", "LOGITECH_C310_RIGHT"]
devices_config = [["TOP", 0, 0, -ROBOT_HEIGHT // 2], ["LEFT", 90, -ROBOT_WIDTH // 2, 0], ["BOT", -90, ROBOT_WIDTH // 2, 0], ["RIGHT", 180, 0, +ROBOT_HEIGHT // 2]]


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


images = []

for index, device in enumerate(devices):
    ###linux
    ret, camera_id = connectCamera(device)
    if ret:
        config = devices_config[index]
        cam = cv.VideoCapture(camera_id)
        cam.set(cv.cv.CV_CAP_PROP_FPS, 10)
        cam.set(cv.cv.CV_CAP_PROP_FRAME_WIDTH, 160)
        cam.set(cv.cv.CV_CAP_PROP_FRAME_HEIGHT, 120)
        print cam.get(cv.cv.CV_CAP_PROP_FRAME_WIDTH)
        print cam.get(cv.cv.CV_CAP_PROP_FRAME_HEIGHT)
        images.append(ImageStream(config[0], cam, config[1], config[2], config[3]))

    ###mac
    # config = devices_config[index]
    # cam = cv.VideoCapture(1)
    # images.append(ImageStream(config[0], cam, config[1], config[2], config[3]))

for img in images:
    print img.name
    t = time.time()
    img.camera.read()
    print time.time() - t