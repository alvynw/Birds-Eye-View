import numpy as np
import cv2 as cv
import glob
import subprocess

cmd = "readlink -f /dev/LOGITECH_C310_BOT"
process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
# output of form /dev/videoX
out = process.communicate()[0]

# parse for ints
nums = [int(x) for x in out if x.isdigit()]

cap = cv.VideoCapture(nums[0])
counter = 0

def main():
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        #print(ret)
	if ret is True:
		frame = cv.resize(frame, (320, 240))
		cv.imshow('resized', frame)

		rows, cols, ch = frame.shape

		#print("rows:", rows, "cols: ", cols, "ch: ", ch)

		src = np.float32([[170 // 2, 480 // 2], [207 // 2, 301 // 2], [436 // 2, 301 // 2], [473 // 2, 480 // 2]])

		dst = np.float32([[430 // 4, 960 // 4], [430 // 4, 540 // 4], [850 // 4, 540 // 4], [850 // 4, 960 // 4]])

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
