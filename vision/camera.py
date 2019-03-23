import numpy as np
import cv2 as cv
import subprocess


print cv.__version__

cmd = "readlink -f /dev/LOGITECH_C310_BOT"
process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
# output of form /dev/videoX
out = process.communicate()[0]

# parse for ints
nums = [int(x) for x in out if x.isdigit()]

cap = cv.VideoCapture(1)
print "hello"

# cap.set(cv.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
# cap.set(cv.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)

counter = 0

factor = 2

def main():
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        #print(ret)
	if ret is True:
		#frame = cv.resize(frame, (320, 240))
		cv.imshow('resized', frame)

		rows, cols, ch = frame.shape

		print("rows:", rows, "cols: ", cols, "ch: ", ch)

		# 2560x1920 -- almost full
		src = np.float32([[478, 1920], [903, 253], [1639, 253], [2035, 1920]]) // factor

		dst = np.float32([[980, 1920], [980, 367], [1580, 367], [1580, 1920]]) // factor

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
