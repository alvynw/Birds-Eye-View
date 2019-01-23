import cv2 as cv
import numpy as np
import math
from config import ROBOT_HEIGHT, ROBOT_WIDTH, IMG_COLS, IMG_ROWS, images


# ccw
def rotate_image(image, angle):
	image_center = tuple(np.array(image.shape[1::-1]) / 2)
	rot_mat = cv.getRotationMatrix2D(image_center, angle, 1.0)
	result = cv.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv.INTER_LINEAR)
	return result


def add_buffer(image):
	rows, cols, ch = image.shape
	border = int(math.sqrt(rows ** 2 + cols ** 2))
	horizontal_buffer = border - cols
	vertical_buffer = border - rows
	new = cv.copyMakeBorder(image, vertical_buffer // 2, vertical_buffer // 2, horizontal_buffer // 2, horizontal_buffer // 2, cv.BORDER_CONSTANT, value=(0, 0, 0))
	return new


# rotate ccw
# degrees
def rotate_point(center_x, center_y, point_x, point_y, theta):
	theta = theta * np.pi / 180
	rotated_x = (point_x - center_x) * math.cos(theta) + (point_y - center_y) * math.sin(theta) + center_x
	rotated_y = (point_x - center_x) * -math.sin(theta) + (point_y - center_y) * math.cos(theta) + center_y
	return [int(rotated_x), int(rotated_y)]


# dst should be larger than src
def add_image(src, dst, dst_x, dst_y, src_x, src_y):
	src_rows, src_cols, src_ch = src.shape

	roi = dst[dst_y - src_y:dst_y + (src_rows - src_y), dst_x - src_x: dst_x + (src_cols - src_x), :]

	src_gray = cv.cvtColor(src, cv.COLOR_RGB2GRAY)

	ret, mask = cv.threshold(src_gray, 10, 255, cv.THRESH_BINARY)
	mask_inv = cv.bitwise_not(mask)

	# Now black-out the area of logo in ROI
	dst_bg = cv.bitwise_and(roi, roi, mask=mask_inv)
	# Take only region of logo from logo image.
	src_fg = cv.bitwise_and(src, src, mask=mask)

	combined = cv.add(dst_bg, src_fg)

	dst[dst_y - src_y:dst_y + (src_rows - src_y), dst_x - src_x: dst_x + (src_cols - src_x), :] = combined
	return dst


# cameras is an array of arrays.
# The array takes in the videostream, the x and y location on the final image, and the orientation
def get_stitched_image(image_streams, robot_width=118, robot_height=118, img_cols=320, img_rows=240):

	images = [img.camera.read() for img in image_streams]

	for idx, img in enumerate(images):
		if img[0] is False:
			print("Could not read ", image_streams[idx].name)

	images[:] = [img for img in images if img[0] is True]

	images[:] = [img[1] for img in images] # to only keep the stream

	images[:] = [cv.resize(img, (img_cols, img_rows)) for img in images]

	images[:] = [cv.cvtColor(img, cv.COLOR_BGR2RGB) for img in images]

	src = np.float32([[46 // 4, 642 // 4], [272 // 4, 395 // 4], [924 // 4, 395 // 4], [1184 // 4, 642 // 4]])
	dst = np.float32([[430 // 4, 960 // 4], [430 // 4, 540 // 4], [850 // 4, 540 // 4], [850 // 4, 960 // 4]])

	M = cv.getPerspectiveTransform(src, dst)

	warped_images = [cv.warpPerspective(img, M, (img_cols, img_rows)) for img in images]

	buffered_image_size = int(math.sqrt(img_rows ** 2 + img_cols ** 2))

	birds_eye = np.zeros((buffered_image_size * 2 + robot_width, buffered_image_size * 2 + robot_height, 3), dtype=np.uint8)

	for idx, img in enumerate(warped_images):
		theta = image_streams[idx].rotation
		x_shift = image_streams[idx].x_shift
		y_shift = image_streams[idx].y_shift
		img = add_buffer(img)
		img = rotate_image(img, theta)

		# point assumed to be bottom center of the image
		img_point = rotate_point(img.shape[1] // 2, img.shape[0] // 2, img.shape[1] // 2, img.shape[0] - (buffered_image_size - img_rows) // 2, theta)

		add_image(img, birds_eye, birds_eye.shape[1] // 2 + x_shift, birds_eye.shape[0] // 2  - y_shift, img_point[0], img_point[1])

	return birds_eye


def main():
	try:
		while True:
			cv.imshow('Birds Eye View', get_stitched_image(images, ROBOT_WIDTH, ROBOT_HEIGHT, IMG_COLS, IMG_ROWS))
			cv.waitKey(1)
	except KeyboardInterrupt:
		print "\nStopping program."

if __name__ == "__main__":
	main()


