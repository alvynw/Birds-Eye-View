import cv2 as cv
import numpy as np
import math
from config import ROBOT_HEIGHT, ROBOT_WIDTH, IMG_COLS, IMG_ROWS, images, transformation_src, transformation_dst


# ccw
def rotate_image(image, angle):
    dist_x, dist_y = find_bounds(image, angle)
    dst = np.zeros((dist_x, dist_y), dtype=np.uint8)
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv.getRotationMatrix2D(image_center, angle, 1.0)
    rot_mat[0][2] += dst.shape[0] // 2 - image.shape[1] // 2
    rot_mat[1][2] += dst.shape[1] // 2 - image.shape[0] // 2
    result = cv.warpAffine(image, rot_mat, (dist_x, dist_y), flags=cv.INTER_LINEAR)

    special_point = rotate_point(image.shape[1] // 2, image.shape[0] // 2, image.shape[1] // 2, image.shape[0], angle,
                                 dist_x // 2 - image.shape[1] // 2, dist_y // 2 - image.shape[0] // 2)
    return [result, special_point]


def find_bounds(image, angle):
    top_right_point = rotate_point(0, 0, image.shape[1] // 2, image.shape[0] // 2, angle)
    bottom_left_point = rotate_point(0, 0, -image.shape[1] // 2, -image.shape[0] // 2, angle)

    top_left_point = rotate_point(0, 0, -image.shape[1] // 2, image.shape[0] // 2, angle)
    bottom_right_point = rotate_point(0, 0, image.shape[1] // 2, -image.shape[0] // 2, angle)

    min_x = min(top_right_point[0], min(bottom_left_point[0], min(top_left_point[0], bottom_right_point[0])))
    max_x = max(top_right_point[0], max(bottom_left_point[0], max(top_left_point[0], bottom_right_point[0])))

    min_y = min(top_right_point[1], min(bottom_left_point[1], min(top_left_point[1], bottom_right_point[1])))
    max_y = max(top_right_point[1], max(bottom_left_point[1], max(top_left_point[1], bottom_right_point[1])))

    dist_x = max_x - min_x
    dist_y = max_y - min_y

    return [dist_x, dist_y]


# rotate ccw
# degrees
def rotate_point(center_x, center_y, point_x, point_y, theta, shift_x=0, shift_y=0):
    theta = theta * np.pi / 180
    rotated_x = (point_x - center_x) * math.cos(theta) + (point_y - center_y) * math.sin(theta) + center_x
    rotated_y = (point_x - center_x) * -math.sin(theta) + (point_y - center_y) * math.cos(theta) + center_y
    return [int(rotated_x) + shift_x, int(rotated_y) + shift_y]


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
    # t = time.time()
    imgs = [img.camera.read() for img in image_streams]
    # print "hello", time.time() - t

    for idx, img in enumerate(imgs):
        if img[0] is False:
            print "Could not read %s image" % (image_streams[idx].name)

    imgs[:] = [img for img in imgs if img[0] is True]

    imgs[:] = [img[1] for img in imgs]  # to only keep the stream

    imgs[:] = [cv.resize(img, (img_cols, img_rows)) for img in imgs]


    M = cv.getPerspectiveTransform(transformation_src, transformation_dst)

    warped_images = [cv.warpPerspective(img, M, (img_cols, img_rows)) for img in imgs]

    x = robot_width
    y = robot_height
    robot_center_x = x // 2
    robot_center_y = y // 2

    for idx, img in enumerate(warped_images):
        theta = image_streams[idx].rotation
        x_shift = image_streams[idx].x_shift
        y_shift = image_streams[idx].y_shift
        dst = find_bounds(img, theta)
        special_point = rotate_point(img.shape[1] // 2, img.shape[0] // 2, img.shape[1] // 2, img.shape[0], theta,
                                     dst[0] // 2 - img.shape[1] // 2, dst[1] // 2 - img.shape[0] // 2)
        # x
        x_pos = robot_center_x + x_shift
        y_pos = robot_center_y + y_shift

        if x_pos < special_point[0]:
            x += special_point[0] - x_pos
            robot_center_x += special_point[0] - x_pos

        x_pos = robot_center_x + x_shift
        if x_pos + dst[0] - special_point[0] > x:
            x += x_pos + dst[0] - special_point[0] - x

        if y_pos < special_point[1]:
            y += special_point[1] - y_pos
            robot_center_y += special_point[1] - y_pos

        y_pos = robot_center_y + y_shift
        if y_pos + dst[1] - special_point[1] > y:
            y += y_pos + dst[1] - special_point[1] - y

    birds_eye = np.zeros((y, x, 3), dtype=np.uint8)

    for idx, img in enumerate(warped_images):
        theta = image_streams[idx].rotation
        x_shift = image_streams[idx].x_shift
        y_shift = image_streams[idx].y_shift
        rotated_img, img_point = rotate_image(img, theta)
        add_image(rotated_img, birds_eye, robot_center_x + x_shift, robot_center_y + y_shift, img_point[0], img_point[1])

    return birds_eye


def main():
    try:
        print images
        while True:
            cv.imshow('Birds Eye View', get_stitched_image(images, ROBOT_WIDTH, ROBOT_HEIGHT, IMG_COLS, IMG_ROWS))
            cv.waitKey(1)
    except KeyboardInterrupt:
        print "\nStopping program."


if __name__ == "__main__":
    main()