import numpy as np
rotaion_xz = []
rotaion_yz = []
cos = []
sin = []

for angle in range(360):
    angle = np.deg2rad(angle)
    c = np.cos(angle)
    s = np.sin(angle)
    cos.append(c)
    sin.append(s)
    rotaion_xz.append(np.array([
        [c, 0, -s],
        [0, 1, 0],
        [s, 0, c]
    ]))
    rotaion_yz.append(np.array([
        [1, 0, 0],
        [0, c, -s],
        [0, s, c]
    ]))

