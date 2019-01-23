# x and y are the respective distances from (0,0) where (0,0) corresponds to the ROBOTS center
# a positive x_shift and y_shift correspond to going right and up respectively
class ImageStream:
    def __init__(self, name, camera, rotation, x_shift, y_shift):
        self.name = name
        self.camera = camera
        self.rotation = rotation
        self.x_shift = x_shift
        self.y_shift = y_shift
