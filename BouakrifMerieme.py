import pygame
import numpy as np
import sys
from utils import *

pygame.init()
height = 600
width = 1000
screen = pygame.display.set_mode((width, height))
f = 2
alpha = 100
beta = 100

grass_top = pygame.image.load('texture/green.png')
grass = pygame.image.load('texture/grass.png')
green = pygame.image.load('texture/green.png')


class Cube:
    def __init__(self, center, size, top_texture, side_texture, bottom_texture):
        self.center = np.array(center)
        self.size = size
        self.top_texture = top_texture
        self.side_texture = side_texture
        self.bottom_texture = bottom_texture
        self.points = self.generate_points()

    def generate_points(self):
        points = np.array([
            [-1, -1, -1, 1],
            [1, -1, -1, 1],
            [1, 1, -1, 1],
            [-1, 1, -1, 1],
            [-1, -1, 1, 1],
            [1, -1, 1, 1],
            [1, 1, 1, 1],
            [-1, 1, 1, 1]
        ]).T
        transform_matrix = np.array([
            [self.size, 0, 0, self.center[0]],
            [0, self.size, 0, self.center[1]],
            [0, 0, self.size, self.center[2]]
        ])
        return np.dot(transform_matrix, points).T


def transform_points(points):
    points_x = points[..., 0]
    points_y = points[..., 1]
    points_z = (points[..., 2])
    points_z[points_z < 0.001] = 0.001
    return np.column_stack((points_x / points_z, points_y / points_z, np.ones(len(points))))


def save_surfaces(transformed_coordinates):
    return sorted([
        [[0, np.linalg.norm(transformed_coordinates[0]), transformed_coordinates[0]],
         [1, np.linalg.norm(transformed_coordinates[1]), transformed_coordinates[1]],
         [2, np.linalg.norm(transformed_coordinates[2]), transformed_coordinates[2]],
         [3, np.linalg.norm(transformed_coordinates[3]), transformed_coordinates[3]]],
        [[4, np.linalg.norm(transformed_coordinates[4]), transformed_coordinates[4]],
         [5, np.linalg.norm(transformed_coordinates[5]), transformed_coordinates[5]],
         [6, np.linalg.norm(transformed_coordinates[6]), transformed_coordinates[6]],
         [7, np.linalg.norm(transformed_coordinates[7]), transformed_coordinates[7]]],
        [[0, np.linalg.norm(transformed_coordinates[0]), transformed_coordinates[0]],
         [1, np.linalg.norm(transformed_coordinates[1]), transformed_coordinates[1]],
         [5, np.linalg.norm(transformed_coordinates[5]), transformed_coordinates[5]],
         [4, np.linalg.norm(transformed_coordinates[4]), transformed_coordinates[4]]],  # top
        [[2, np.linalg.norm(transformed_coordinates[2]), transformed_coordinates[2]],
         [3, np.linalg.norm(transformed_coordinates[3]), transformed_coordinates[3]],
         [7, np.linalg.norm(transformed_coordinates[7]), transformed_coordinates[7]],
         [6, np.linalg.norm(transformed_coordinates[6]), transformed_coordinates[6]]],  # bottom
        [[5, np.linalg.norm(transformed_coordinates[5]), transformed_coordinates[5]],
         [1, np.linalg.norm(transformed_coordinates[1]), transformed_coordinates[1]],
         [2, np.linalg.norm(transformed_coordinates[2]), transformed_coordinates[2]],
         [6, np.linalg.norm(transformed_coordinates[6]), transformed_coordinates[6]], ],
        [[4, np.linalg.norm(transformed_coordinates[4]), transformed_coordinates[4]],
         [0, np.linalg.norm(transformed_coordinates[0]), transformed_coordinates[0]],
         [3, np.linalg.norm(transformed_coordinates[3]), transformed_coordinates[3]],
         [7, np.linalg.norm(transformed_coordinates[7]), transformed_coordinates[7]], ]
    ], key=lambda x: np.mean([i[1] for i in x]), reverse=True)[-3:]


def lerp(p1, p2, f):
    return p1 + f * (p2 - p1)


def lerp2d(p1, p2, f):
    return tuple(lerp(p1[i], p2[i], f) for i in range(2))


def draw_quad(surface, quad, img, intensity):
    points = dict()
    w = img.get_size()[0]
    h = img.get_size()[1]

    for i in range(h + 1):
        b = lerp2d(quad[1], quad[2], i / h)
        c = lerp2d(quad[0], quad[3], i / h)
        for u in range(w + 1):
            a = lerp2d(c, b, u / w)
            points[(u, i)] = a
    for x in range(w):
        for y in range(h):
            pygame.draw.polygon(
                surface,
                np.array(img.get_at((x, y))) * intensity,
                [points[(a, b)] for a, b in [(x, y), (x, y + 1), (x + 1, y + 1), (x + 1, y)]]
            )


def draw_cube(screen, cube, angle_x_z, angle_y_z, player_position, f, K, side, top, bottom, intensity=None):
    global rotaion_xz, rotaion_yz
    transformed_points = np.dot(np.dot(cube.points - player_position, rotaion_xz[int(angle_x_z) % 360]),
                                rotaion_yz[int(angle_y_z) % 360])
    surfaces = save_surfaces(transformed_points)
    points_2d = np.dot(transform_points(transformed_points), K)
    f = 0
    for index, surface in enumerate(surfaces):
        if surface[0][2][2] > f and surface[1][2][2] > f and surface[2][2][2] > f and surface[3][2][2] > f:
            if intensity is None:
                intensity = 1
            p = []
            for point, _, _ in surface:
                p.append(points_2d[point])
            if surface[0][0] == 0 and surface[1][0] == 1 and surface[2][0] == 5 and surface[3][0] == 4:
                draw_quad(screen, p, top, intensity)
            elif surface[0][0] == 2 and surface[1][0] == 3 and surface[2][0] == 7 and surface[3][0] == 6:
                draw_quad(screen, p, bottom, intensity)
            else:
                draw_quad(screen, p, side, intensity)


def main():
    cubes = [
        Cube(center=(-2, 2, -2), size=2, top_texture=green, side_texture=grass, bottom_texture=grass),
        Cube(center=(0, 2, -2), size=2, top_texture=green, side_texture=grass, bottom_texture=grass),
        Cube(center=(2, 2, -2), size=2, top_texture=green, side_texture=grass, bottom_texture=grass),
        Cube(center=(-2, 2, 0), size=2, top_texture=green, side_texture=grass, bottom_texture=grass),
        Cube(center=(0, 2, 0), size=2, top_texture=green, side_texture=grass, bottom_texture=grass),
        Cube(center=(2, 2, 0), size=2, top_texture=green, side_texture=grass, bottom_texture=grass),
        Cube(center=(-2, 2, 2), size=2, top_texture=green, side_texture=grass, bottom_texture=grass),
        Cube(center=(0, 2, 2), size=2, top_texture=green, side_texture=grass, bottom_texture=grass),
        Cube(center=(2, 2, 2), size=2, top_texture=green, side_texture=grass, bottom_texture=grass),

        Cube(center=(-2, 0, -2), size=2, top_texture=green, side_texture=grass, bottom_texture=grass),
        Cube(center=(0, 0, -2), size=2, top_texture=green, side_texture=grass, bottom_texture=grass),
        Cube(center=(2, 0, -2), size=2, top_texture=green, side_texture=grass, bottom_texture=grass),
        Cube(center=(-2, 0, 0), size=2, top_texture=green, side_texture=grass, bottom_texture=grass),

    ]

    camera_position = [0, 0, -10]
    xz = 0
    yz = 0
    u0 = width // 2
    v0 = height // 2
    K = np.array([[f * alpha, 0, u0], [0, f * beta, v0]]).T
    jump_force = 0
    jump_reduce = 0.1
    gravity = 1
    clock = pygame.time.Clock()

    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            camera_position[2] += 1
            camera_position[0] -= 1
        if keys[pygame.K_s]:
            camera_position[2] -= 1
            camera_position[0] += 1

        if keys[pygame.K_LEFT]:
            xz += 1
        if keys[pygame.K_RIGHT]:
            xz -= 1
        if keys[pygame.K_UP]:
            camera_position[1] += 1
        if keys[pygame.K_DOWN]:
            camera_position[1] -= 1

        if keys[pygame.K_SPACE]:
            if jump_force == 0:
                jump_force = 2
        jump_force = max(0, jump_force - jump_reduce)
        camera_position[1] = min(0, camera_position[1] - jump_force + gravity)

        xz %= 180
        yz %= 180
        for cube in cubes:
            draw_cube(screen, cube, xz, yz, camera_position, f, K, cube.side_texture, cube.top_texture,
                      cube.bottom_texture)
        clock.tick(60)
        pygame.display.set_caption("FPS: " + str(round(clock.get_fps())))
        pygame.display.update()


if __name__ == '__main__':
    main()

