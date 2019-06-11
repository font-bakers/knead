from collections import deque
import numpy as np
from knead.utils import font_pb2


# pylint: disable=R0914
def sample_quadratic_bezier(control_points, num_steps):
    """
    control_points : [num_curves, 3, 2]
    num_steps : int
    """
    num_steps += 1
    num_curves = control_points.shape[0]
    steps = np.linspace(0, num_steps * num_curves, num_steps)
    steps, _ = np.modf(steps)
    control_point_0 = control_points[:, 0]
    control_point_1 = control_points[:, 1]
    control_point_2 = control_points[:, 2]

    j = 0
    previous_i = 0
    samples = np.zeros((num_steps - 1, 2), np.float32)
    for i in range(num_steps):
        # pylint: disable=C0103
        if (steps[i] < steps[i - 1]) and (i > 0):
            s = steps[previous_i:i][..., np.newaxis]
            a = control_point_0[j][np.newaxis, :]
            b = control_point_1[j][np.newaxis, :]
            c = control_point_2[j][np.newaxis, :]
            z = b + (1 - s) ** 2 * (a - b) + s ** 2 * (c - b)
            samples[previous_i:i] = z
            previous_i = i
            j += 1

    return samples


def read(buf, max_num_pts_per_contour, num_samples):
    glyph_proto = font_pb2.glyph()

    with open(buf, "rb") as f:
        glyph_proto.ParseFromString(f.read())

    glyph = glyph_proto.glyph[0]  # pylint: disable=E1101
    bezier_points = deque(glyph.bezier_points)
    num_pts_per_contour = glyph.contour_locations

    if (
        (not num_pts_per_contour)
        or (len(num_pts_per_contour) > 3)
        or (max(num_pts_per_contour) > max_num_pts_per_contour)
    ):
        raise RuntimeError("Something bad happened")

    contours = np.zeros((3, num_samples, 2), np.float32)

    for i, num_pts in enumerate(num_pts_per_contour):
        pts = np.array([bezier_points.popleft() for _ in range(num_pts * 6)])
        contour = pts.reshape([-1, 6]).reshape(-1, 3, 2)
        contours[i] = sample_quadratic_bezier(contour, num_samples)

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


def proto_to_npy(file_to):
    pass
