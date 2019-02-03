import cv2 as cv
from image_stream import ImageStream

ROBOT_WIDTH = 446
ROBOT_HEIGHT = 446
IMG_COLS = 640
IMG_ROWS = 480

top_cam = cv.VideoCapture(1)
left_cam = cv.VideoCapture(2)
# right_cam = cv.VideoCapture(3)
bot_cam = cv.VideoCapture(0)

top = ImageStream("top", top_cam, 0, 0, ROBOT_HEIGHT // 2)
left = ImageStream("left", left_cam, 90, -ROBOT_WIDTH // 2, 0)

bot = ImageStream("right", bot_cam, 180, 0, -ROBOT_HEIGHT // 2)

images = [top, left, bot]

# x is 127.5 deg from base
#        cam
#       /
# ____x/
