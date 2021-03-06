from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
from PIL import Image
import StringIO
from stitching import get_stitched_image
from config import ROBOT_HEIGHT, ROBOT_WIDTH, IMG_COLS, IMG_ROWS, images, counter
import cv2
import thread
import glob
from threading import Thread
import sys
import time

class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('.mjpg'):
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            while True:
                try:
                    birds_eye = get_stitched_image(images, ROBOT_WIDTH, ROBOT_HEIGHT, IMG_COLS, IMG_ROWS)
                    birds_eye = cv2.cvtColor(birds_eye, cv2.COLOR_BGR2RGB)
                    jpg = Image.fromarray(birds_eye)
                    tmp_file = StringIO.StringIO()
                    jpg.save(tmp_file, 'JPEG')
                    self.wfile.write("--jpgboundary")
                    self.send_header('Content-type', 'image/jpeg')
                    self.send_header('Content-length', str(jpg.size))
                    self.end_headers()
                    jpg.save(self.wfile, 'JPEG')
                except KeyboardInterrupt:
                    break
            return
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('<html><title>Bird\'s Eye View</title><head></head><h2>Bird\'s Eye View</h2><body><p>')
            self.wfile.write('<img src=".mjpg"/>')
            self.wfile.write('</p></body></html>')
        return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    '''Threads stuff'''

toRun = True

def checkNewCam():
    while toRun:
	time.sleep(0.5)
    	if len(glob.glob("/dev/video*")) != counter:
    	    print "New video device detected"
    	    print "Interrupting main thread"
	    thread.interrupt_main()
	    sys.exit(0)

def main():
    HOST = '10.8.46.21'  # localhost
    PORT = 8080
    print "starting checking thread"
    thread = Thread(target=checkNewCam, args=())
    thread.start()
    print "finished starting checking thread"
    try:
        server = HTTPServer((HOST, PORT), CamHandler)
        print "Server started at ", HOST, " port ", PORT
        server.serve_forever()
    except KeyboardInterrupt:
    	print "Keyboard interrupt"
        server.socket.close()
        global toRun
        toRun = False
        print "Server cancelled at ", HOST, "port ", PORT
    except IOError:
    	print "IO Error"
        print "Server closed at ", HOST, "port ", PORT


if __name__ == "__main__":
    main()
