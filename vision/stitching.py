import cv2 as cv
import numpy as np
import math

#ccw
def rotateImage(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv.INTER_LINEAR)
  return result

def addBuffer(image):
    rows, cols, ch = image.shape
    border = int(math.sqrt(rows ** 2 + cols ** 2))
    horizontal_buffer = border - cols
    vertical_buffer = border - rows
    new = cv.copyMakeBorder(image, vertical_buffer // 2, vertical_buffer // 2, horizontal_buffer // 2,
                            horizontal_buffer // 2, cv.BORDER_CONSTANT, value=(0, 0, 0))
    return [new, horizontal_buffer, vertical_buffer]

#rotate ccw
def rotatePoint(center_x, center_y, point_x, point_y, theta):
    theta = theta*np.pi/180
    rotated_x = (point_x-center_x) * math.cos(theta) + (point_y - center_y) * math.sin(theta) + center_x
    rotated_y = (point_x-center_x) * -math.sin(theta) + (point_y - center_y) * math.cos(theta) + center_y
    return [int(rotated_x), int(rotated_y)]

#dst should be larger than src
def addImage(src, dst, dst_x, dst_y, src_x, src_y):
    src_rows, src_cols, src_ch = src.shape
    dst[dst_y - src_y:dst_y + (src_rows - src_y), dst_x - src_x : dst_x + (src_cols - src_x),:] \
        = cv.add(dst[dst_y - src_y:dst_y + (src_rows - src_y), dst_x - src_x : dst_x + (src_cols - src_x),:], src[:, :, :])
    return src

top_stream = cv.VideoCapture(0)
left_stream = cv.VideoCapture(1)

ROBOT_WIDTH = 470
ROBOT_HEIGHT = 470

if __name__ == "__main__":
    while(True):
        # Capture frame-by-frame
        top_ret, top_frame = top_stream.read()
        left_ret, left_frame = left_stream.read()
        right_frame = np.full((960, 1280, 3), 255, dtype=np.uint8)
        bot_frame = np.full((960, 1280, 3), 255, dtype=np.uint8)

        top_frame = cv.resize(top_frame, (640, 480))
        left_frame = cv.resize(left_frame, (640, 480))
        right_frame = cv.resize(right_frame, (640, 480))
        bot_frame = cv.resize(bot_frame, (640, 480))

        rows, cols, ch = top_frame.shape
        # print("rows:", rows, "cols: ", cols, "ch: ", ch)

        src = np.float32([[46 // 2, 642 // 2], [272 // 2, 395 // 2], [924 // 2, 395 // 2], [1184 // 2, 642 // 2]])
        dst = np.float32([[430 // 2, 960 // 2], [430 // 2, 540 // 2], [850 // 2, 540 // 2], [850 // 2, 960 // 2]])

        M = cv.getPerspectiveTransform(src, dst)

        top = cv.warpPerspective(top_frame, M, (cols, rows))
        left = cv.warpPerspective(left_frame, M, (cols, rows))
        right = cv.warpPerspective(right_frame, M, (cols, rows))
        bot = cv.warpPerspective(bot_frame, M, (cols, rows))

        bufferedImageSize = int(math.sqrt(rows ** 2 + cols ** 2))

        birds_eye = np.zeros((bufferedImageSize * 2 + ROBOT_WIDTH, bufferedImageSize * 2 + ROBOT_HEIGHT, 3), dtype = np.uint8)

        top, top_horizontal_buffer, top_vertical_buffer = addBuffer(top)
        top = rotateImage(top, 135)
        top_point = rotatePoint(top.shape[1] // 2, top.shape[0] // 2, top.shape[1] // 2,
                                top.shape[0] - top_vertical_buffer // 2, 135)
        addImage(top, birds_eye, birds_eye.shape[1] // 2, birds_eye.shape[0] // 2, top_point[0], top_point[1])

        left, left_horizontal_buffer, left_vertical_buffer = addBuffer(top)
        left = rotateImage(left, 45)
        left_point = rotatePoint(left.shape[1] // 2, left.shape[0] // 2, left.shape[1] // 2,
                                left.shape[0] - left_vertical_buffer // 2, 45)
        addImage(left, birds_eye, birds_eye.shape[1] // 2, birds_eye.shape[0] // 2, left_point[0], left_point[1])

        cv.imshow('birds eye', birds_eye)

        key = cv.waitKey(1)
        if key & 0xFF == ord('q'):
            break

    top_stream.release()
    left_stream.release()
    cv.destroyAllWindows()
