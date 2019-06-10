# /bin/python

import os
import glob
import font_pb2
import numpy as np

from tqdm import tqdm
from collections import deque


def sample_qb(control_points, num_steps):
    # I hate this function WOW
    num_steps = num_steps + 1
    num_curves = control_points.shape[0]
    steps = np.linspace(0, num_steps * num_curves, num_steps)
    steps, _ = np.modf(steps)
    P0 = control_points[:, 0]
    P1 = control_points[:, 1]
    P2 = control_points[:, 2]

    j = 0
    prev_look = 0
    samples = np.zeros((num_steps - 1, 2), np.float32)
    for i in range(num_steps):
        if (i > 0) and (steps[i] < steps[i - 1]):
            s = steps[prev_look:i]
            s = s[..., np.newaxis]
            a = P0[j][np.newaxis, :]
            b = P1[j][np.newaxis, :]
            c = P2[j][np.newaxis, :]
            z = b + (1 - s) ** 2 * (a - b) + s ** 2 * (c - b)
            samples[prev_look:i] = z
            prev_look = i
            j += 1

    return samples


def read(buf, max_num_pts_per_contour, num_samples):
    glyph_proto = font_pb2.glyph()
    glyph_proto.ParseFromString(open(buf, "rb").read())
    glyph = glyph_proto.glyph[0]
    bezier_points = deque(glyph.bezier_points)
    num_pts_per_contour = glyph.contour_locations

    if not num_pts_per_contour:
        return None

    if len(num_pts_per_contour) > 3:
        return None

    if max(num_pts_per_contour) > max_num_pts_per_contour:
        return None
    else:
        contours = np.zeros((3, num_samples, 2), np.float32)
        for i, num_pts in enumerate(num_pts_per_contour):
            pts = np.array([bezier_points.popleft() for _ in range(num_pts * 6)])
            contour = pts.reshape([-1, 6]).reshape(-1, 3, 2)
            contours[i] = sample_qb(contour, num_samples)

        return contours


written = 0
num_shards = 128
num_samples = 640
for a in tqdm(glob.glob("./filteredas/*")):
    contours = read(a, 60, num_samples)
    if contours is not None:
        path = "with_{}_samples/{}/{}".format(
            num_samples, written % num_shards, written
        )
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

        np.save(path, contours, allow_pickle=False)
        written += 1
