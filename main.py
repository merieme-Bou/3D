import pygame
import math

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load texture
texture = pygame.image.load('texture/bricks.png').convert_alpha()

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

class Engine:

 def __init__(self):
  self.mesh_cube = Mesh()
  self.projection_matrix = Mat4x4()
  self.theta = 0
  self.camera_position = Vec3D(0, 0, 0,0)
  self.fov = 90  # Initial field of view

 def multiply_matrix_vector(self, v_in, v_out, m):
    v_out.x = v_in.x * m.m[0][0] + v_in.y * m.m[1][0] + v_in.z * m.m[2][0] + m.m[3][0]
    v_out.y = v_in.x * m.m[0][1] + v_in.y * m.m[1][1] + v_in.z * m.m[2][1] + m.m[3][1]
    v_out.z = v_in.x * m.m[0][2] + v_in.y * m.m[1][2] + v_in.z * m.m[2][2] + m.m[3][2]



 def init_cube(self):
    self.mesh_cube.tris = [

        #south
         Triangle(Vec3D(0, 0, 0, 1), Vec3D(0, 1, 0, 1), Vec3D(1, 1, 0, 1), Vec2D(0,1), Vec2D(0,0), Vec2D(1,0) ),
         Triangle(Vec3D(0, 0, 0, 1), Vec3D(1, 1, 0, 1), Vec3D(1, 0, 0, 1), Vec2D(0,1), Vec2D(1,0), Vec2D(1,1) ),
#east
         Triangle(Vec3D(1, 0, 0, 1), Vec3D(1, 1, 0, 1), Vec3D(1, 1, 1, 1), Vec2D(0,1), Vec2D(0,0), Vec2D(1,0) ),
         Triangle(Vec3D(1, 0, 0, 1), Vec3D(1, 1, 1, 1), Vec3D(1, 0, 1, 1), Vec2D(0,1), Vec2D(1,0), Vec2D(1,1) ),
#north
         Triangle(Vec3D(1, 0, 1, 1), Vec3D(1, 1, 1, 1), Vec3D(0, 1, 1, 1), Vec2D(0,1), Vec2D(0,0), Vec2D(1,0) ),
         Triangle(Vec3D(1, 0, 1, 1), Vec3D(0, 1, 1, 1), Vec3D(0, 0, 1, 1), Vec2D(0,1), Vec2D(1,0), Vec2D(1,1) ),

         Triangle(Vec3D(0, 0, 1, 1), Vec3D(0, 1, 1, 1), Vec3D(0, 1, 0, 1), Vec2D(0,1), Vec2D(0,0), Vec2D(1,0) ),
         Triangle(Vec3D(0, 0, 1, 1), Vec3D(0, 1, 0, 1), Vec3D(0, 0, 0, 1), Vec2D(0,1), Vec2D(1,0), Vec2D(1,1) ),

         Triangle(Vec3D(0, 1, 0, 1), Vec3D(0, 1, 1, 1), Vec3D(1, 1, 1, 1), Vec2D(0,1), Vec2D(0,0), Vec2D(1,0) ),
         Triangle(Vec3D(0, 1, 0, 1), Vec3D(1, 1, 1, 1), Vec3D(1, 1, 0, 1), Vec2D(0,1), Vec2D(1,0), Vec2D(1,1) ),

         Triangle(Vec3D(1, 0, 1, 1), Vec3D(0, 0, 1, 1), Vec3D(0, 0, 0, 1), Vec2D(0,1), Vec2D(0,0), Vec2D(1,0) ),
         Triangle(Vec3D(1, 0, 1, 1), Vec3D(0, 0, 0, 1), Vec3D(1, 0, 0, 1), Vec2D(0,1), Vec2D(1,0), Vec2D(1,1) )
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
        self.multiply_matrix_vector(tri.p[0], tri.p[0], rotation_z)
        self.multiply_matrix_vector(tri.p[1], tri.p[1], rotation_z)
        self.multiply_matrix_vector(tri.p[2], tri.p[2], rotation_z)

        # rotate in X
        self.multiply_matrix_vector(tri.p[0], tri.p[0], rotation_x)
        self.multiply_matrix_vector(tri.p[1], tri.p[1], rotation_x)
        self.multiply_matrix_vector(tri.p[2], tri.p[2], rotation_x)

        # translate
        translated = Triangle(Vec3D(tri.p[0].x, tri.p[0].y, tri.p[0].z+100,tri.p[0].w),
                              Vec3D(tri.p[1].x, tri.p[1].y, tri.p[1].z+100,tri.p[1].w ),
                              Vec3D(tri.p[2].x, tri.p[2].y, tri.p[2].z+100,tri.p[2].w),
                              Vec2D(tri.t[0].u, tri.t[0].v),
                              Vec2D(tri.t[1].u, tri.t[1].v),
                              Vec2D(tri.t[2].u, tri.t[2].u))
        # Use Cross-Product to get surface normal
        vCamera = Vec3D(0, 0, 0,1)  # Replace with your camera position
        normal = Vec3D(0, 0, 0,1)
        line1 = Vec3D(translated.p[1].x - translated.p[0].x,
                      translated.p[1].y - translated.p[0].y,
                      translated.p[1].z - translated.p[0].z,1)

        line2 = Vec3D(translated.p[2].x - translated.p[0].x,
                      translated.p[2].y - translated.p[0].y,
                      translated.p[2].z - translated.p[0].z,1)

        normal.x = line1.y * line2.z - line1.z * line2.y
        normal.y = line1.z * line2.x - line1.x * line2.z
        normal.z = line1.x * line2.y - line1.y * line2.x

        # Normalize the normal
        l = math.sqrt(normal.x * normal.x + normal.y * normal.y + normal.z * normal.z)
        normal.x /= l
        normal.y /= l
        normal.z /= l

        # Check condition
        if (normal.x * (translated.p[0].x - vCamera.x) +
                normal.y * (translated.p[0].y - vCamera.y) +
                normal.z * (translated.p[0].z - vCamera.z) < 0.0):
            # project
            self.multiply_matrix_vector(translated.p[0], translated.p[0], self.projection_matrix)
            self.multiply_matrix_vector(translated.p[1], translated.p[1], self.projection_matrix)
            self.multiply_matrix_vector(translated.p[2], translated.p[2], self.projection_matrix)

            # scale to view
            projected = translated
            projected.p[0].x += 1
            projected.p[0].y += 1
            projected.p[1].x += 1
            projected.p[1].y += 1
            projected.p[2].x += 1
            projected.p[2].y += 1

            projected.p[0].x *= 0.5 * SCREEN_WIDTH
            projected.p[0].y *= 0.5 * SCREEN_HEIGHT
            projected.p[1].x *= 0.5 * SCREEN_WIDTH
            projected.p[1].y *= 0.5 * SCREEN_HEIGHT
            projected.p[2].x *= 0.5 * SCREEN_WIDTH
            projected.p[2].y *= 0.5 * SCREEN_HEIGHT


            # Adjust coordinates based on camera position
            translated.p[0].x += self.camera_position.x
            translated.p[0].y += self.camera_position.y
            translated.p[0].z += self.camera_position.z

            translated.p[1].x += self.camera_position.x
            translated.p[1].y += self.camera_position.y
            translated.p[1].z += self.camera_position.z

            translated.p[2].x += self.camera_position.x
            translated.p[2].y += self.camera_position.y
            translated.p[2].z += self.camera_position.z

            # Triangle vertices & texture coords
            v1, v2, v3 = tri.p
            t1, t2, t3 = tri.t

            for x in range(0, SCREEN_WIDTH):

                for y in range(0, SCREEN_HEIGHT):
                    # Barycentric coords
                    alpha = (v2.y - v3.y) * (x - v3.x) + (v3.x - v2.x) * (y - v3.y)
                    beta = (v3.y - v1.y) * (x - v3.x) + (v1.x - v3.x) * (y - v3.y)
                    gamma = 1.0 - alpha - beta

                    # Interpolate texture coords
                    tex_u = t1.u * alpha + t2.u * beta + t3.u * gamma
                    tex_v = t1.v * alpha + t2.v * beta + t3.v * gamma

                    # Get texture dimensions
                    tex_width = texture.get_width()
                    tex_height = texture.get_height()

                    # Cast to integers
                    tex_u_int = int(tex_u)
                    tex_v_int = int(tex_v)

                    # Clamp to texture bounds
                    tex_u_int = max(0, min(tex_u_int, tex_width - 1))
                    tex_v_int = max(0, min(tex_v_int, tex_height - 1))

                    # Sample texture
                    color = texture.get_at((tex_u_int, tex_v_int))

                     # Draw colored triangle
            pygame.draw.polygon(screen, color,
                                [(translated.p[0].x, translated.p[0].y),
                                 (translated.p[1].x, translated.p[1].y),
                                 (translated.p[2].x, translated.p[2].y)])



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