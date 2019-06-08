def not_repeat(glyph, font_dict):
    """
    This function will return False when a lowercase glyph is a copy of the
    uppercase glyph from the same font.

    Paramaters
    ----------
    glyph: the character we are trying to asses
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
    pass
