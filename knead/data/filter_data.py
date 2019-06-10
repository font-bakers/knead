# /bin/python

import glob
import font_pb2

from shutil import copy
from tqdm import tqdm


def read(buf, max_num_pts_per_contour):
    glyph_proto = font_pb2.glyph()
    glyph_proto.ParseFromString(open(buf, "rb").read())
    glyph = glyph_proto.glyph[0]
    num_pts_per_contour = glyph.contour_locations

    if not num_pts_per_contour:
        return ""

    if max(num_pts_per_contour) < max_num_pts_per_contour:
        return buf
    else:
        return ""


passing = list(filter(None, [read(a, 60) for a in glob.glob("./allas/*")]))

[copy(p, "./filteredas/") for p in tqdm(passing)]
