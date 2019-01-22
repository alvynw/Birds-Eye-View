import cv2 as cv
import numpy as np
import math
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
from PIL import Image
import StringIO

top_stream = cv.VideoCapture(0)
left_stream = cv.VideoCapture(1)
ROBOT_WIDTH = 118
ROBOT_HEIGHT = 118

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

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	'''Threads stuff'''

def main(): 
	HOST = '' # localhost
	PORT = 8080

	global top_stream
	global left_stream

	try: 
		server = ThreadedHTTPServer((HOST, PORT), CamHandler)
		print("Server started at ", HOST, "port ", PORT)
		server.serve_forever()
	except KeyboardInterrupt:
		top_stream.release()
		left_stream.release()
		server.socket.close()

class CamHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		print("Users wants to get something")
		if self.path.endswith('.mjpg'):
			self.send_response(200)
			self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
			self.end_headers()
			while(True):
				try:
					# Capture frame-by-frame
					top_ret, top_frame = top_stream.read()
					left_ret, left_frame = left_stream.read()
					
					top_frame=cv.cvtColor(top_frame,cv.COLOR_BGR2RGB)
					left_frame=cv.cvtColor(left_frame,cv.COLOR_BGR2RGB)

					if (not top_ret or not left_ret): continue

					right_frame = np.full((960, 1280, 3), 255, dtype=np.uint8)
					bot_frame = np.full((960, 1280, 3), 255, dtype=np.uint8)

					top_frame = cv.resize(top_frame, (320, 240))
					left_frame = cv.resize(left_frame, (320, 240))
					right_frame = cv.resize(right_frame, (320, 240))
					bot_frame = cv.resize(bot_frame, (320, 240))

					rows, cols, ch = top_frame.shape
					# print("rows:", rows, "cols: ", cols, "ch: ", ch)

					src = np.float32([[46 // 4, 642 // 4], [272 // 4, 395 // 4], [924 // 4, 395 // 4], [1184 // 4, 642 // 4]])
					dst = np.float32([[430 // 4, 960 // 4], [430 // 4, 540 // 4], [850 // 4, 540 // 4], [850 // 4, 960 // 4]])

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

					left, left_horizontal_buffer, left_vertical_buffer = addBuffer(left)
					left = rotateImage(left, 45)
					left_point = rotatePoint(left.shape[1] // 2, left.shape[0] // 2, left.shape[1] // 2,
								left.shape[0] - left_vertical_buffer // 2, 45)
								
					addImage(left, birds_eye, birds_eye.shape[1] // 2, birds_eye.shape[0] // 2, left_point[0], left_point[1])
					
					jpg = Image.fromarray(birds_eye)
					tmpFile = StringIO.StringIO()
					jpg.save(tmpFile,'JPEG')
					self.wfile.write("--jpgboundary")
					self.send_header('Content-type','image/jpeg')
					self.send_header('Content-length',str(tmpFile.len))
					self.end_headers()
					jpg.save(self.wfile,'JPEG')
				except KeyboardInterrupt:
					break
			return
		else:
			print("html")
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write('<html><head>Bird\'s Eye View</head>')
			self.wfile.write('<img src="http://127.0.0.1:8080/as.mjpg"/>')
			self.wfile.write('<img src="http://127.0.0.1:8080/s.mjpg"/>')
			self.wfile.write('</html>')
		return

if __name__ == "__main__":
	main()


