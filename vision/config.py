import cv2 as cv
from image_stream import ImageStream
import subprocess
import time
import re

# 320 x 240
# 80 Degrees from the base


IMG_COLS = 320
IMG_ROWS = 240

ROBOT_WIDTH = 200
ROBOT_HEIGHT = 200

SMALL_TRAPEZOID_LENGTH = 150

devices = ["LOGITECH_C310_TOP", "LOGITECH_C310_LEFT", "LOGITECH_C310_RIGHT", "LOGITECH_C310_BOT"]
devices_config = [["TOP", 0, 0, -ROBOT_HEIGHT // 2], ["LEFT", 90, -ROBOT_WIDTH // 2, 0], ["RIGHT", -90, ROBOT_WIDTH // 2, 0], ["BOT", 180, 0, +ROBOT_HEIGHT // 2]]


def connectCamera(device):
    cmd = "readlink -f /dev/%s" % (device)
    print cmd
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    # output of form /dev/videoX
    time.sleep(0.25)
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
    ###mac
    config = devices_config[index]
    cam = cv.VideoCapture(1)
    images.append(ImageStream(config[0], cam, config[1], config[2], config[3]))

    ###linux

    # ret, camera_id = connectCamera(device)
    # if ret:
    #     config = devices_config[index]
    #     cam = cv.VideoCapture(camera_id)
    #     images.append(ImageStream(config[0], cam, config[1], config[2], config[3]))

