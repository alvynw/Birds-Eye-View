import numpy as np
import cv2 as cv
import glob

cap = cv.VideoCapture(1)
counter = 0

def main():
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        #frame = cv.resize(frame, (640, 480))
        cv.imshow('resized', frame)

        rows, cols, ch = frame.shape

        print("rows:", rows, "cols: ", cols, "ch: ", ch)

        src = np.float32([[94 * 2, 480 * 2], [226 * 2, 268 * 2], [409 * 2, 269 * 2], [548 * 2, 480 * 2]])

        dst = np.float32([[286 * 2, 480 * 2], [286 * 2, 320 * 2], [354 * 2, 320 * 2], [354 * 2, 480 * 2]])

        M = cv.getPerspectiveTransform(src, dst)

        transformed = cv.warpPerspective(frame, M, (cols, rows))


        key = cv.waitKey(1)
        # Display the resulting frame
        cv.imshow('warped', transformed)

        if key & 0xFF == ord('q'):
            break

        global counter

        if key & 0xFF == ord('y'): #save on pressing 'y'
            cv.imwrite('../images/calibration/calibration_image_%s.bmp' % counter,frame)
            counter +=1

    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
