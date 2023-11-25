import pygame
import math

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Vec3D:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

class Triangle:
  def __init__(self, p1, p2, p3):
    self.p1 = p1
    self.p2 = p2
    self.p3 = p3
class Mesh:
    def __init__(self):
        self.tris = []

class Mat4x4:
 def __init__(self):
  self.m = [[0] * 4 for _ in range(4)]

class Engine:

 def __init__(self):
  self.mesh_cube = Mesh()
  self.projection_matrix = Mat4x4()
  self.theta = 0


 def multiply_matrix_vector(self, v_in, v_out, m):
    v_out.x = v_in.x * m.m[0][0] + v_in.y * m.m[1][0] + v_in.z * m.m[2][0] + m.m[3][0]
    v_out.y = v_in.x * m.m[0][1] + v_in.y * m.m[1][1] + v_in.z * m.m[2][1] + m.m[3][1]
    v_out.z = v_in.x * m.m[0][2] + v_in.y * m.m[1][2] + v_in.z * m.m[2][2] + m.m[3][2]



 def init_cube(self):
    self.mesh_cube.tris = [

        #south
         Triangle(Vec3D(0, 0, 0), Vec3D(0, 1, 0), Vec3D(1, 1, 0)),
         Triangle(Vec3D(0, 0, 0), Vec3D(1, 1, 0), Vec3D(1, 0, 0)),
#east
         Triangle(Vec3D(1, 0, 0), Vec3D(1, 1, 0), Vec3D(1, 1, 1)),
         Triangle(Vec3D(1, 0, 0), Vec3D(1, 1, 1), Vec3D(1, 0, 1)),
#north
         Triangle(Vec3D(1, 0, 1), Vec3D(1, 1, 1), Vec3D(0, 1, 1)),
         Triangle(Vec3D(1, 0, 1), Vec3D(0, 1, 1), Vec3D(0, 0, 1)),

         Triangle(Vec3D(0, 0, 1), Vec3D(0, 1, 1), Vec3D(0, 1, 0)),
         Triangle(Vec3D(0, 0, 1), Vec3D(0, 1, 0), Vec3D(0, 0, 0)),

         Triangle(Vec3D(0, 1, 0), Vec3D(0, 1, 1), Vec3D(1, 1, 1)),
         Triangle(Vec3D(0, 1, 0), Vec3D(1, 1, 1), Vec3D(1, 1, 0)),

         Triangle(Vec3D(1, 0, 1), Vec3D(0, 0, 1), Vec3D(0, 0, 0)),
         Triangle(Vec3D(1, 0, 1), Vec3D(0, 0, 0), Vec3D(1, 0, 0))
     ]


    # projection matrix setup
    near = 0.1
    far = 100
    fov = 90
    aspect = SCREEN_HEIGHT / SCREEN_WIDTH
    fov_rad = 1 / math.tan(fov * math.pi / 360)

    self.projection_matrix.m[0][0] = aspect * fov_rad
    self.projection_matrix.m[1][1] = fov_rad
    self.projection_matrix.m[2][2] = far / (far - near)
    self.projection_matrix.m[3][2] = -far * near / (far - near)
    self.projection_matrix.m[2][3] = 1
    self.projection_matrix.m[3][3] = 0


 def render(self):
    # clear display
    screen.fill((0, 0, 0))

    # rotation matrices
    rotation_z = Mat4x4()
    rotation_x = Mat4x4()

    self.theta += 0.005

    # Z rotation
    rotation_z.m[0][0] = math.cos(self.theta)
    rotation_z.m[0][1] = -math.sin(self.theta)
    rotation_z.m[1][0] = math.sin(self.theta)
    rotation_z.m[1][1] = math.cos(self.theta)
    rotation_z.m[2][2] = 1
    rotation_z.m[3][3] = 1

    # X rotation
    rotation_x.m[0][0] = 1
    rotation_x.m[1][1] = math.cos(self.theta)
    rotation_x.m[1][2] = -math.sin(self.theta)
    rotation_x.m[2][1] = math.sin(self.theta)
    rotation_x.m[2][2] = math.cos(self.theta)
    rotation_x.m[3][3] = 1


    # draw triangles
    for tri in self.mesh_cube.tris:
        # rotate in Z
        self.multiply_matrix_vector(tri.p1, tri.p1, rotation_z)
        self.multiply_matrix_vector(tri.p2, tri.p2, rotation_z)
        self.multiply_matrix_vector(tri.p3, tri.p3, rotation_z)

        # rotate in X
        self.multiply_matrix_vector(tri.p1, tri.p1, rotation_x)
        self.multiply_matrix_vector(tri.p2, tri.p2, rotation_x)
        self.multiply_matrix_vector(tri.p3, tri.p3, rotation_x)

        # translate
        translated = Triangle(Vec3D(tri.p1.x, tri.p1.y, tri.p1.z+2),
                              Vec3D(tri.p2.x, tri.p2.y, tri.p2.z+2 ),
                              Vec3D(tri.p3.x, tri.p3.y, tri.p3.z+2))

        # project
        self.multiply_matrix_vector(translated.p1, translated.p1, self.projection_matrix)
        self.multiply_matrix_vector(translated.p2, translated.p2, self.projection_matrix)
        self.multiply_matrix_vector(translated.p3, translated.p3, self.projection_matrix)

        # scale to view
        projected = translated
        projected.p1.x += 1
        projected.p1.y += 1
        projected.p2.x += 1
        projected.p2.y += 1
        projected.p3.x += 1
        projected.p3.y += 1

        projected.p1.x *= 0.5 * SCREEN_WIDTH
        projected.p1.y *= 0.5 * SCREEN_HEIGHT
        projected.p2.x *= 0.5 * SCREEN_WIDTH
        projected.p2.y *= 0.5 * SCREEN_HEIGHT
        projected.p3.x *= 0.5 * SCREEN_WIDTH
        projected.p3.y *= 0.5 * SCREEN_HEIGHT
        # draw triangle
        print(projected.p1.x, projected.p1.y)
        # draw lines between triangle points
        pygame.draw.line(screen, (0, 255, 255), (projected.p1.x, projected.p1.y), (projected.p2.x, projected.p2.y))
        pygame.draw.line(screen, (0, 255, 255), (projected.p2.x, projected.p2.y), (projected.p3.x, projected.p3.y))
        pygame.draw.line(screen, (0, 255, 255), (projected.p3.x, projected.p3.y), (projected.p1.x, projected.p1.y))


engine = Engine()

running = True
clock = pygame.time.Clock()
while running:
 clock.tick(10)
 for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False



    # Render the updated scene
 engine.init_cube()
 engine.render()

    # Update the display
 pygame.display.update()
pygame.quit()