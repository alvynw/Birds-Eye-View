import cv2
import numpy as np
from matplotlib import pyplot as plt
import glob

img = cv2.imread("../images/70degree test image.bmp")

rows, cols, ch = img.shape

print("rows:",rows, "cols: ", cols, "ch: ", ch)

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((9*6,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('../images/calibration/*.bmp')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (9,6),None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        print(ret)
        objpoints.append(objp)
        cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners)
        # Draw and display the corners
        cv2.drawChessboardCorners(img, (9,6), corners,ret)
        cv2.imshow('img',img)
        cv2.waitKey(500)

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
'''
print("mtx: ", mtx)
print("dist: ", dist)
print("rvecs: ", rvecs)
print("tvecs: ", tvecs)
'''

test_img = cv2.imread('../images/70degree test image.bmp')
h,  w = test_img.shape[:2]
newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

# undistort
undistorted = cv2.undistort(test_img, mtx, dist, None, newcameramtx)

# crop the image
x,y,w,h = roi
undistorted = undistorted[y:y+h, x:x+w]


src = np.float32([[46, 642], [272, 395], [924, 395], [1184, 642]])

dst = np.float32([[430, 960], [430, 540], [850, 540], [850, 960]])

M = cv2.getPerspectiveTransform(src, dst)

transformed = cv2.warpPerspective(undistorted, M, (cols, rows))

plt.subplot(121)
plt.imshow(undistorted)
plt.subplot(122)
plt.imshow(transformed)
plt.show()

