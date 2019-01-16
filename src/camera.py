import numpy as np
import cv2 as cv

cap = cv.VideoCapture(1)
counter = 0;

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    rows, cols, ch = frame.shape
    #print(ret)

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_RGB)
    #rows, cols, ch = frame.shape

    #print("rows:", rows, "cols: ", cols, "ch: ", ch)

    src = np.float32([[46, 642], [272, 395], [924, 395], [1184, 642]])

    dst = np.float32([[430, 960], [430, 540], [850, 540], [850, 960]])

    M = cv.getPerspectiveTransform(src, dst)

    transformed = cv.warpPerspective(frame, M, (cols, rows))


    key = cv.waitKey(1)
    print(key)
    # Display the resulting frame
    cv.imshow('warped', transformed)
    cv.imshow('original', frame)
    if key & 0xFF == ord('q'):
        break


    if key & 0xFF == ord('y'): #save on pressing 'y'
        cv.imwrite(f'../images/calibration/calibration_image_{counter}.bmp',frame)
        counter +=1

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()