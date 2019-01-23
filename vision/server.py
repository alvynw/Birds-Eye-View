from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
from PIL import Image
import StringIO
from stitching import get_stitched_image
from config import ROBOT_HEIGHT, ROBOT_WIDTH, IMG_COLS, IMG_ROWS, images


class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("Users wants to get something")
        if self.path.endswith('.mjpg'):
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()

            while True:
                try:
                    birds_eye = get_stitched_image(images, ROBOT_WIDTH, ROBOT_HEIGHT, IMG_COLS, IMG_ROWS)
                    jpg = Image.fromarray(birds_eye)
                    tmpFile = StringIO.StringIO()
                    jpg.save(tmpFile, 'JPEG')
                    self.wfile.write("--jpgboundary")
                    self.send_header('Content-type', 'image/jpeg')
                    self.send_header('Content-length', str(tmpFile.len))
                    self.end_headers()
                    jpg.save(self.wfile, 'JPEG')
                except KeyboardInterrupt:
                    break
            return
        else:
            print("html")
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('<html><title>Bird\'s Eye View</title><head></head><h2>Bird\'s Eye View</h2><body><p>')
            self.wfile.write('<img src=".mjpg"/>')
            self.wfile.write('</p></body></html>')
        return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    '''Threads stuff'''


def main():
    HOST = ''  # localhost
    PORT = 8080

    try:
        server = ThreadedHTTPServer((HOST, PORT), CamHandler)
        print("Server started at ", HOST, "port ", PORT)
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()


if __name__ == "__main__":
    main()
