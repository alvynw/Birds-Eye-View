import cv2 as cv
from image_stream import ImageStream
import subprocess
import time

ROBOT_WIDTH = 223
ROBOT_HEIGHT = 223
IMG_COLS = 320
IMG_ROWS = 240

suffixes = ["TOP", "LEFT", "RIGHT", "BOT"]

def connectCamera(suffix):
	cmd = "readlink -f /dev/LOGITECH_C310_%s" % (suffix) 
	process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
	print process
	# output of form /dev/videoX
	time.sleep(5)
	t = process.poll()
	if (t is not None):
		out = process.communicate()[0]
		print "process is not none"
		# parse for ints
		nums = [int(x) for x in out if x.isdigit()]
		return [True, nums[0]]
	else:
		print "process is none"
		proc.kill()
		print(suffix)
		return [False, -1]

bot_cam = cv.VideoCapture(connectCamera("BOT")[1])

#top = ImageStream("top", top_cam, 0, 0, ROBOT_HEIGHT // 2)
#left = ImageStream("left", left_cam, 90, -ROBOT_WIDTH // 2, 0)

bot = ImageStream("right", bot_cam, 180, 0, -ROBOT_HEIGHT // 2)

images = [bot]

# x is 127.5 deg from base
#        cam
#       /
# ____x/
