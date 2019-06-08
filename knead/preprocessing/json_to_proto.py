import sys
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


def pkl2protos(proto_dir, pickle_name, file_num):
    """
    This function takes one pickle and proto directory and puts all of its
    glyphs into protos in the proto dir

    Parameters
    ----------
    proto_dir: the directory where all the protos should be saved

    pickle: the location of the pickle to be put into protos
    """
    try:
        with open(pickle_name, "rb") as font_string:
            font_dict = pickle.load(font_string)
            for glyph in font_dict:
                # basically we are going to flatten everything into just an
                # array of points.
                # we will keep track of the location of where each contour stops
                # so we can reconstruct on the other end.
                proto = font_pb2.glyph()
                if glyph in CHARACTER_SET and not_repeat(glyph, font_dict):
                    contours = font_dict[glyph]
                    num_contours = len(contours)
                    points = []
                    contour_locations = []
                    for _, c in contours.items():
                        contour_locations.append(len(c))
                        for curve in c:
                            for point in curve:
                                points += point
                    # write it in
                    new_glyph = proto.glyph.add()
                    new_glyph.num_contours = num_contours
                    points = list(points)
                    new_glyph.bezier_points.extend(points)
                    new_glyph.contour_locations.extend(contour_locations)
                    new_glyph.font_name = pickle_name
                    new_glyph.glyph_name = glyph

                    # save it up
                    with open("{}/{}{}".format(proto_dir, glyph, file_num), "ab") as f:
                        f.write(proto.SerializeToString())

    except Exception as err:
        print(pickle_name, err, sys.exc_info()[0])


def json_to_proto(file_from, file_to):
    pass
