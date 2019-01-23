import numpy as np
import cv2 as cv

cap = cv.VideoCapture(1)
counter = 0

def main():
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        frame = cv.resize(frame, (640, 480))

        rows, cols, ch = frame.shape

        print("rows:", rows, "cols: ", cols, "ch: ", ch)

        src = np.float32([[46 // 2, 642 // 2], [272 // 2, 395 // 2], [924 // 2, 395 // 2], [1184 // 2, 642 // 2]])

        dst = np.float32([[430 // 2, 960 // 2], [430 // 2, 540 // 2], [850 // 2, 540 // 2], [850 // 2, 960 // 2]])

        M = cv.getPerspectiveTransform(src, dst)

        transformed = cv.warpPerspective(frame, M, (cols, rows))


        key = cv.waitKey(1)
        # Display the resulting frame
        cv.imshow('warped', transformed)
        cv.imshow('original', frame)
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
