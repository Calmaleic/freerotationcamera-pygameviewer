class Camera:
  def __init__(self, pos, fsize, angles, fov):
    self.pos = pos
    self.fsize = fsize
    self.eulerAngles = angles
    self.fov = fov