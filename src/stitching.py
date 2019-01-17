import cv2 as cv
import numpy as np

top = cv.VideoCapture(2)
left = cv.VideoCapture(1)

ROBOT_SIZE = 470

while(True):
    # Capture frame-by-frame
    top_ret, top_frame = top.read()
    left_ret, left_frame = left.read()

    right_frame = np.full((960, 1280, 3), 255, dtype= np.uint8)
    bot_frame = np.full((960, 1280, 3), 255, dtype= np.uint8)


    rows, cols, ch = top_frame.shape
    # print("rows:", rows, "cols: ", cols, "ch: ", ch)

    src = np.float32([[46, 642], [272, 395], [924, 395], [1184, 642]])
    dst = np.float32([[430, 960], [430, 540], [850, 540], [850, 960]])

    # src = np.float32([[46/2, 642/2], [272/2, 395/2], [924/2, 395/2], [1184/2, 642/2]])
    # dst = np.float32([[430/2, 960/2], [430/2, 540/2], [850/2, 540/2], [850/2, 960/2]])

    M = cv.getPerspectiveTransform(src, dst)

    top_transform = cv.warpPerspective(top_frame, M, (cols, rows))
    left_transform = cv.rotate(cv.warpPerspective(left_frame, M, (cols, rows)), cv.ROTATE_90_COUNTERCLOCKWISE)
    right_transform = cv.rotate(cv.warpPerspective(right_frame, M, (cols, rows)), cv.ROTATE_90_CLOCKWISE)
    bot_transform = cv.rotate(cv.warpPerspective(right_frame, M, (cols, rows)), cv.ROTATE_180)

    # cv.imshow('top', top_transform)
    # cv.imshow('left', left_transform)

    birds_eye = np.zeros((rows * 2 + ROBOT_SIZE, rows * 2 + ROBOT_SIZE, 3), dtype = np.uint8)

    birds_eye_length = birds_eye.shape[0]

    # CLOSE_SIDE = range(birds_eye_length // 2 - (cols - ROBOT_SIZE) // 2 - ROBOT_SIZE // 2, birds_eye_length // 2 + (cols - ROBOT_SIZE) // 2 + ROBOT_SIZE // 2)

    birds_eye[:rows, birds_eye_length // 2 - (cols - ROBOT_SIZE) // 2 - ROBOT_SIZE // 2: birds_eye_length // 2 + (
                cols - ROBOT_SIZE) // 2 + ROBOT_SIZE // 2, :top_transform.shape[2]] = cv.add(birds_eye[:rows, birds_eye_length // 2 - (cols - ROBOT_SIZE) // 2 - ROBOT_SIZE // 2: birds_eye_length // 2 + (cols - ROBOT_SIZE) // 2 + ROBOT_SIZE // 2, :top_transform.shape[2]], top_transform)
    birds_eye[birds_eye_length // 2 - (cols - ROBOT_SIZE) // 2 - ROBOT_SIZE // 2: birds_eye_length // 2 + (
                cols - ROBOT_SIZE) // 2 + ROBOT_SIZE // 2, :rows, :top_transform.shape[2]] = cv.add(birds_eye[birds_eye_length // 2 - (cols - ROBOT_SIZE) // 2 - ROBOT_SIZE // 2: birds_eye_length // 2 + (cols - ROBOT_SIZE) // 2 + ROBOT_SIZE // 2, :rows, :top_transform.shape[2]], left_transform)
    birds_eye[birds_eye_length // 2 - (cols - ROBOT_SIZE) // 2 - ROBOT_SIZE // 2: birds_eye_length // 2 + (
                cols - ROBOT_SIZE) // 2 + ROBOT_SIZE // 2, birds_eye_length - rows:birds_eye_length,
    :top_transform.shape[2]] = cv.add(birds_eye[birds_eye_length // 2 - (cols - ROBOT_SIZE) // 2 - ROBOT_SIZE // 2: birds_eye_length // 2 + (cols - ROBOT_SIZE) // 2 + ROBOT_SIZE // 2, birds_eye_length - rows:birds_eye_length, :top_transform.shape[2]], right_transform)
    birds_eye[birds_eye_length - rows:birds_eye_length,
    birds_eye_length // 2 - (cols - ROBOT_SIZE) // 2 - ROBOT_SIZE // 2: birds_eye_length // 2 + (
                cols - ROBOT_SIZE) // 2 + ROBOT_SIZE // 2, :top_transform.shape[2]] = cv.add(birds_eye[birds_eye_length - rows:birds_eye_length, birds_eye_length // 2 - (cols - ROBOT_SIZE) // 2 - ROBOT_SIZE // 2: birds_eye_length // 2 + (cols - ROBOT_SIZE) // 2 + ROBOT_SIZE // 2, :top_transform.shape[2]], bot_transform)

    cv.imshow('birds eye', birds_eye)

    key = cv.waitKey(1)
    if key & 0xFF == ord('q'):
        break

top.release()
left.release()
cv.destroyAllWindows()
