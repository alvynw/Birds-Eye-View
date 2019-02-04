import numpy as np
import cv2 as cv
import glob
import subprocess

cmd = "readlink -f /dev/LOGITECH_C310_BOT"
process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
print process
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
		frame = cv.resize(frame, (640, 480))
		cv.imshow('resized', frame)

		rows, cols, ch = frame.shape

		#print("rows:", rows, "cols: ", cols, "ch: ", ch)

		src = np.float32([[94, 480], [226, 268], [409, 269], [548, 480]])

		dst = np.float32([[286, 480], [286, 320], [354, 320], [354, 480]])

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
