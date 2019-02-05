import cv2 as cv
from image_stream import ImageStream
import subprocess
import time

ROBOT_WIDTH = 223
ROBOT_HEIGHT = 223
IMG_COLS = 320
IMG_ROWS = 240

devices = ["LOGITECH_C310_TOP", "LOGITECH_C310_LEFT", "LOGITECH_C310_RIGHT", "LOGITECH_C310_BOT"]
devices_config = [["TOP", 0, 0, ROBOT_HEIGHT // 2], ["LEFT", 90, -ROBOT_WIDTH // 2, 0 ], ["RIGHT", -90, ROBOT_WIDTH // 2, 0], ["BOT", 180, 0, -ROBOT_HEIGHT // 2]]

def connectCamera(device):
	cmd = "readlink -f /dev/%s" % (device) 
	process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
	print process
	# output of form /dev/videoX
	time.sleep(0.25)
	t = process.poll()
	if (t is not None):
		out = process.communicate()[0]
		device_re = re.compile("^\\dev\\video(\d+)")
		if (device_re.match(out)):
			video_id = device_re.group(1)
			return [True, video_id]
		else:
			print "%s not found" % (device)				
	else:
		print "%s not found" % (device)
	proc.kill()
	return [False, -1]
images = []

for index, device in enumerate(devices):
	ret, camera_id = connectCamera(device)
	if (ret):
		config = devices_config[index]
		images.append(ImageStream(config[0], VideoCapture(camera_id), config[1], config[2], config[3])



# x is 127.5 deg from base
#        cam
#       /
# ____x/
