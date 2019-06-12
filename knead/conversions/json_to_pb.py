import os
import json
from itertools import chain
from knead.utils import glyph_batch_pb2, CHARACTER_SET, UPPERCASES, LOWERCASES


def format_file_with_character(file_to, character):
    """
    Format the file path with an appropriately formatted character string. This
    is necessary because some file systems are case sensitive by default, but
    others are not: thus, writing to both a `Helvetica.A.pb` and
    `Helvetica.a.pb` is not feasible.

    Parameters
    ----------
    file_to : string
        Path to file that is being written to. E.g. "data/Helvetica.pb"
    character : string
        Character that is being saved. E.g. "a"

    Returns
    -------
    file_to_with_glyph : string
        New path to file with properly formatted character.
        E.g. "data/Helvetica.a_lower.pb"
    """
    if character in UPPERCASES:
        formatted_character = character.upper() + "_upper"
    elif character in LOWERCASES:
        formatted_character = character.lower() + "_lower"
    else:
        formatted_character = character

    root, extension = os.path.splitext(file_to)
    file_to_with_glyph = root + "." + formatted_character + extension
    return file_to_with_glyph


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
    if glyph in LOWERCASES and glyph.upper() in font_dict:
        lower_contours = font_dict[glyph]
        upper_contours = font_dict[glyph.upper()]
        if lower_contours == upper_contours:
            return False
    return True


def json_to_pb(file_from, file_to):
    with open(file_from, "r") as f:
        font_dict = json.load(f)

    for character in font_dict:
        # Basically we are going to flatten everything into just an
        # array of points. We will keep track of the location of where each
        # contour stops so we can reconstruct on the other end.
        protobuf = glyph_batch_pb2.Batch()

        if character in CHARACTER_SET and not_repeat(character, font_dict):
            contours = font_dict[character]
            num_points_in_contours = []
            points = []

            for contour in contours:
                num_points_in_contours.append(len(contour))
                points.extend(list(chain.from_iterable(chain.from_iterable(contour))))

            # Write it in
            new_glyph = protobuf.glyphs.add()  # pylint: disable=E1101
            new_glyph.num_contours = len(contours)
            new_glyph.bezier_points.extend(points)
            new_glyph.num_points_in_contours.extend(num_points_in_contours)
            new_glyph.font_name = os.path.split(file_to)[-1]
            new_glyph.glyph_name = character

            # Save each character as a separate .pb file
            file_to_with_glyph = format_file_with_character(file_to, character)
            with open(file_to_with_glyph, "ab+") as f:
                f.write(protobuf.SerializeToString())
