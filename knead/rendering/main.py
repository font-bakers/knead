#!/bin/python

import os
import glob
import font_pb2

import numpy as np
from collections import deque
from pathlib import Path

from tqdm import tqdm
from PIL import Image
import aggdraw


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
        return 2 * [None]

    if len(num_pts_per_contour) > 3:
        return 2 * [None]

    if max(num_pts_per_contour) > max_num_pts_per_contour:
        return 2 * [None]

    else:
        contours = []
        samples = np.zeros((3, num_samples, 2), np.float32)
        bottom = 10
        top = -10
        for i, num_pts in enumerate(num_pts_per_contour):
            pts = np.array([bezier_points.popleft() for _ in range(num_pts * 6)])
            contour = pts.reshape([-1, 6]).reshape(-1, 3, 2)

            if contour.shape[0] == 0:
                return 2 * [None]

            bottom = np.minimum(bottom, np.amin(contour))
            top = np.maximum(top, np.amax(contour))
            contours.append(contour)

        for i, contour in enumerate(contours):
            contours[i] = (contour - bottom) / (top - bottom)
            samples[i] = sample_qb(contours[i], num_samples)

        return contours, samples


def render(out_file, contours, size):
    s = ""
    for contour in contours:
        for i, curve in enumerate(contour):
            for j, pair in enumerate(curve):
                pair = pair * size * 0.8
                pair = pair.astype(np.int32)
                if (i == 0) and (j == 0):
                    s += "M{:d},{:d} ".format(pair[0], pair[1])
                elif j == 1:
                    s += "Q{:d},{:d}".format(pair[0], pair[1])
                elif j == 2:
                    s += ",{:d},{:d} ".format(pair[0], pair[1])

    img = Image.new("RGB", (size, size))
    draw = aggdraw.Draw(img)
    outline = aggdraw.Pen("white", 1)
    fill = aggdraw.Brush("white")

    symbol = aggdraw.Symbol(s)

    pos = int(0.1 * size)
    xy = (pos, pos)
    draw.symbol(xy, symbol, outline, fill)
    draw.flush()
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img.save(out_file)


written = 0
num_shards = 512
num_samples = 160
size = 128
path = "/zooper1/fontbakers/data/renders/{}_samples_3/".format(num_samples)
input_glob_string = "/zooper1/fontbakers/data/noCapsnoRepeatsSingleExampleProtos/*"

for a in tqdm(glob.glob(input_glob_string)):
    num_bytes = os.path.getsize(a)
    if num_bytes > 4000:
        continue

    category = "".join([i for i in os.path.basename(a) if not i.isdigit()])

    contours, samples = read(a, 60, num_samples)

    if contours is not None:
        points_path = os.path.join(
            path, "shard_{}/{}.pts".format(written % num_shards, written)
        )
        cat_path = os.path.join(
            path, "shard_{}/{}.cat".format(written % num_shards, written)
        )
        image_path = os.path.join(
            path, "shard_{}/{}.png".format(written % num_shards, written)
        )

        if not os.path.exists(os.path.dirname(points_path)):
            os.makedirs(os.path.dirname(points_path))

        with open(cat_path, "w") as f:
            f.write(category)

        render(image_path, contours, size=size)
        np.save(points_path, samples, allow_pickle=False)
        written += 1

Path(os.path.join(path, "{:d}".format(written))).touch()
