import cv2 as cv
from image_stream import ImageStream

ROBOT_WIDTH = 118
ROBOT_HEIGHT = 118
IMG_COLS = 320
IMG_ROWS = 240

top_cam = cv.VideoCapture(1)
left_cam = cv.VideoCapture(2)
# right_cam = cv.VideoCapture(3)
# bot_cam = cv.VideoCapture(4)

top = ImageStream("top", top_cam, -45, ROBOT_WIDTH // 2, ROBOT_HEIGHT // 2)
left = ImageStream("left", left_cam, -90, ROBOT_WIDTH // 2, ROBOT_HEIGHT // 2)

images = [top, left]
