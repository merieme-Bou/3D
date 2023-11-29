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
  self.camera_position = Vec3D(0, 0, 0)
  self.fov = 90  # Initial field of view

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

 def update_projection_matrix(self):
        near = 0.1
        far = 100
        aspect = SCREEN_HEIGHT / SCREEN_WIDTH
        fov_rad = 1 / math.tan(math.radians(self.fov) / 2)

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
        translated = Triangle(Vec3D(tri.p1.x, tri.p1.y, tri.p1.z+100),
                              Vec3D(tri.p2.x, tri.p2.y, tri.p2.z+100 ),
                              Vec3D(tri.p3.x, tri.p3.y, tri.p3.z+100))
        # Use Cross-Product to get surface normal
        vCamera = Vec3D(0, 0, 0)  # Replace with your camera position
        normal = Vec3D(0, 0, 0)
        line1 = Vec3D(translated.p2.x - translated.p1.x,
                      translated.p2.y - translated.p1.y,
                      translated.p2.z - translated.p1.z)

        line2 = Vec3D(translated.p3.x - translated.p1.x,
                      translated.p3.y - translated.p1.y,
                      translated.p3.z - translated.p1.z)

        normal.x = line1.y * line2.z - line1.z * line2.y
        normal.y = line1.z * line2.x - line1.x * line2.z
        normal.z = line1.x * line2.y - line1.y * line2.x

        # Normalize the normal
        l = math.sqrt(normal.x * normal.x + normal.y * normal.y + normal.z * normal.z)
        normal.x /= l
        normal.y /= l
        normal.z /= l

        # Check condition
        if (normal.x * (translated.p1.x - vCamera.x) +
                normal.y * (translated.p1.y - vCamera.y) +
                normal.z * (translated.p1.z - vCamera.z) < 0.0):
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

            # Illumination
            light_direction = Vec3D(0.0, 0.0, -1.0)
            l = math.sqrt(
                light_direction.x * light_direction.x + light_direction.y * light_direction.y + light_direction.z * light_direction.z)
            light_direction.x /= l
            light_direction.y /= l
            light_direction.z /= l

            # How similar is normal to light direction
            dp = normal.x * light_direction.x + normal.y * light_direction.y + normal.z * light_direction.z

            # Calculate RGB color based on the dot product
            r = int(0 * max(0, dp))
            g = int(255 * max(0, dp))
            b = int(0* max(0, dp))

            # Adjust coordinates based on camera position
            translated.p1.x += self.camera_position.x
            translated.p1.y += self.camera_position.y
            translated.p1.z += self.camera_position.z

            translated.p2.x += self.camera_position.x
            translated.p2.y += self.camera_position.y
            translated.p2.z += self.camera_position.z

            translated.p3.x += self.camera_position.x
            translated.p3.y += self.camera_position.y
            translated.p3.z += self.camera_position.z

            # Draw colored triangle
            pygame.draw.polygon(screen, (r, g, b),
                                [(translated.p1.x, translated.p1.y),
                                 (translated.p2.x, translated.p2.y),
                                 (translated.p3.x, translated.p3.y)])
            # draw lines between triangle points
            pygame.draw.line(screen, (0, 0, 0), (translated.p1.x, translated.p1.y), (translated.p2.x, translated.p2.y))
            pygame.draw.line(screen, (0, 0, 0), (translated.p2.x, translated.p2.y), (translated.p3.x, translated.p3.y))
            pygame.draw.line(screen, (0, 0, 0), (translated.p3.x, translated.p3.y), (translated.p1.x, translated.p1.y))


engine = Engine()

running = True
clock = pygame.time.Clock()
while running:
 clock.tick(40)
 for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
 # Camera controls (you can customize these based on your needs)
 keys = pygame.key.get_pressed()
 if keys[pygame.K_LEFT]:
          engine.camera_position.x -= 1
 if keys[pygame.K_RIGHT]:
          engine.camera_position.x += 1
 if keys[pygame.K_UP]:
          engine.camera_position.y -= 1
 if keys[pygame.K_DOWN]:
          engine.camera_position.y += 1


    # Camera zooming
 if keys[pygame.K_w]:
        engine.fov -= 1  # Increase field of view for zooming in
 if keys[pygame.K_s]:
        engine.fov += 1  # Decrease field of view for zooming out

 # Update the projection matrix with the new FOV
 engine.update_projection_matrix()

    # Render the updated scene
 engine.init_cube()
 engine.render()

    # Update the display
 pygame.display.update()
pygame.quit()