class Vec2D:
    def __init__(self, u, v):
        self.u = u
        self.v = v


class Vec3D:
  def __init__(self, x, y, z, w):
    self.x = x
    self.y = y
    self.z = z
    self.w = w

class Triangle:
  def __init__(self, p0, p1, p2, t0, t1, t2):
        self.p = [p0, p1, p2]
        self.t = [t0, t1, t2]
class Mesh:
    def __init__(self):
        self.tris = []

class Mat4x4:
 def __init__(self):
  self.m = [[0] * 4 for _ in range(4)]