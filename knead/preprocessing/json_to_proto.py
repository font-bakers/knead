import os
import json
from knead.utils import font_pb2, CHARACTER_SET


def not_repeat(glyph, font_dict):
    """
    Returns False when a lowercase glyph is a copy of the uppercase glyph from
    the same font.

    Paramaters
    ----------
    glyph: the character we are trying to assess
    font_dict: the dictionary that contains all the bezier information for a font

    Returns
    -------
    Boolean
        True if the glyph is not a repeat or is not a character we are checking
        False if the glyph is a repeat of its corresponnding uppercase
    """
    lowercase = set("abcdefghijklmnopqrstuvwxyz")
    if glyph in lowercase and glyph.upper() in font_dict:
        lower_contours = font_dict[glyph]
        upper_contours = font_dict[glyph.upper()]
        if lower_contours == upper_contours:
            return False
    return True


def json_to_proto(file_from, file_to):
    with open(file_from, "rb") as f:
        font_dict = json.load(f)

        for glyph in font_dict:
            # Basically we are going to flatten everything into just an
            # array of points. We will keep track of the location of where each
            # contour stops so we can reconstruct on the other end.
            proto = font_pb2.glyph()

            if glyph in CHARACTER_SET and not_repeat(glyph, font_dict):
                contours = font_dict[glyph]
                points = []
                contour_locations = []

                for _, contour in contours.items():
                    contour_locations.append(len(contour))
                    for curve in contour:
                        for point in curve:
                            points += point

                # Write it in
                new_glyph = proto.glyph.add()  # pylint: disable=E1101
                new_glyph.num_contours = len(contours)
                points = list(points)
                new_glyph.bezier_points.extend(points)
                new_glyph.contour_locations.extend(contour_locations)
                new_glyph.font_name = os.path.split(file_to)[-1]
                new_glyph.glyph_name = glyph

                # Save it up
                with open(file_to, "ab+") as f:
                    f.write(proto.SerializeToString())
