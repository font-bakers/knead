from collections import deque
from absl import flags
import numpy as np
from knead.utils import glyph_batch_pb2

FLAGS = flags.FLAGS


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


def read(buf, max_num_points_in_contour, num_samples):
    protobuf = glyph_batch_pb2.Batch()
    with open(buf, "rb") as f:
        protobuf.ParseFromString(f.read())

    glyph = protobuf.glyphs[0]  # pylint: disable=E1101
    bezier_points = deque(glyph.bezier_points)
    num_points_in_contours = glyph.num_points_in_contours

    if len(num_points_in_contours) > 3:
        raise RuntimeError("Glyph contains more than 3 contours.")
    if max(num_points_in_contours) > max_num_points_in_contour:
        raise RuntimeError(
            "Glyph contains contour with more than {} control points.".format(
                max_num_points_in_contour
            )
        )

    contours = np.zeros((3, num_samples, 2), np.float32)
    for i, num_points in enumerate(num_points_in_contours):
        points = np.array([bezier_points.popleft() for _ in range(num_points * 6)])
        contour = points.reshape([-1, 6]).reshape(-1, 3, 2)
        contours[i] = sample_quadratic_bezier(contour, num_samples)

    return contours


def pb_to_npy(file_from, file_to):
    contours = read(file_from, FLAGS.max_num_points_in_contour, FLAGS.num_samples)
    if contours is not None:
        np.save(file_to, contours, allow_pickle=False)
