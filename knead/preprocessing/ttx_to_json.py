from xml.etree import cElementTree
import json
from knead.utils import CHARACTER_SET


def create_point(left_point, right_point, em_value):
    """
    Create a virtual on-point in-between left and right off-points.

    Parameters
    ----------
    left_point : XML object of the left point

    right_point: XML object of the right point

    em_value: size of EM box used to normalize new point

    Returns
    -------
    New XML object that is the midpoint of left and right points
    """
    left_pointx = int(left_point.get("x")) / em_value
    right_pointx = int(right_point.get("x")) / em_value
    new_pointx = round(left_pointx + (right_pointx - left_pointx) / 2, 4)
    left_pointy = int(left_point.get("y")) / em_value
    right_pointy = int(right_point.get("y")) / em_value
    new_pointy = round(left_pointy + (right_pointy - left_pointy) / 2, 4)
    return cElementTree.Element("pt", x=new_pointx, y=new_pointy, on="1")


# pylint: disable=R0912,R0914,R0915
def get_curves(contour, em_value):
    """
    unpack a contour to all of its Bezier curves

    Parameters
    ----------
    contour: XML object of the contour

    em_value : size of EM box, used to normalize points

    Returns
    -------
    Array of Arrays of Bezier curve definitions.
    A Bezier curve definition consists of three points, an on-curve off-curve
    and on-curve point.
    """
    points = contour.findall("pt")
    curves = []
    # check if the first point is zero.
    if points:
        if points[0].get("on") == "0":
            # use the last one as the first one.
            last_point = points.pop()
            if last_point.get("on") == "1":
                # add it to the top
                points = [last_point] + points
            else:
                # create a point in between
                points.append(last_point)
                points = [create_point(points[0], last_point, em_value)] + points
        # now iterate through all the points and build the curves
        loc = 0
        virtual_point = None
        while loc < len(points) - 2:
            current_point = points[loc]
            next_point = points[loc + 1]
            next_next_point = points[loc + 2]
            startx = int(current_point.get("x")) / em_value
            starty = int(current_point.get("y")) / em_value
            nextx = int(next_point.get("x")) / em_value
            nexty = int(next_point.get("y")) / em_value
            lastx = round(int(next_next_point.get("x")) / em_value, 4)
            lasty = round(int(next_next_point.get("y")) / em_value, 4)
            midx = round(startx + (nextx - startx) / 2, 4)
            midy = round(starty + (nexty - starty) / 2, 4)
            startx = round(startx, 4)
            starty = round(starty, 4)
            nextx = round(nextx, 4)
            nexty = round(nexty, 4)
            if virtual_point is not None:
                startx = virtual_point.get("x")
                starty = virtual_point.get("y")
                current_point = virtual_point
                virtual_point = None
            if current_point.get("on") == next_point.get("on") == "1":
                curves.append([(startx, starty), (midx, midy), (nextx, nexty)])
                loc += 1
            elif (
                current_point.get("on") == "1"
                and next_point.get("on") == "0"
                and next_next_point.get("on") == "1"
            ):
                curves.append([(startx, starty), (nextx, nexty), (lastx, lasty)])
                loc += 2
            elif (
                current_point.get("on") == "1"
                and next_point.get("on") == next_next_point.get("on") == "0"
            ):
                virtual_point = create_point(next_point, next_next_point, em_value)
                curves.append(
                    [
                        (startx, starty),
                        (nextx, nexty),
                        (virtual_point.get("x"), virtual_point.get("y")),
                    ]
                )
                loc += 1
            else:
                raise Exception(
                    "unhandled case",
                    current_point.get("on"),
                    next_point.get("on"),
                    next_next_point.get("on"),
                    virtual_point,
                    current_point,
                )
    # deal with end cases
    last = points[-1]
    first = points[0]
    startx = int(first.get("x")) / em_value
    starty = int(first.get("y")) / em_value
    lastx = int(last.get("x")) / em_value
    lasty = int(last.get("y")) / em_value
    if len(points) > 2:
        second_last = points[-2]
        secondx = int(second_last.get("x")) / em_value
        secondy = int(second_last.get("y")) / em_value
        if second_last.get("on") == last.get("on") == "1":
            midx = round(secondx + (lastx - secondx) / 2, 4)
            midy = round(secondy + (lasty - secondy) / 2, 4)
            secondx = round(secondx, 4)
            secondy = round(secondy, 4)
            lastx = round(lastx, 4)
            lasty = round(lasty, 4)
            curves.append([(secondx, secondy), (midx, midy), (lastx, lasty)])
        elif (
            second_last.get("on") == "1"
            and last.get("on") == "0"
            and first.get("on") == "1"
        ):
            startx = round(startx, 4)
            starty = round(starty, 4)
            secondx = round(secondx, 4)
            secondy = round(secondy, 4)
            lastx = round(lastx, 4)
            lasty = round(lasty, 4)
            curves.append([(secondx, secondy), (lastx, lasty), (startx, starty)])
        elif second_last.get("on") == last.get("on") == "0" and first.get("on") == "1":
            virtual_point = create_point(second_last, last, em_value)
            startx = round(startx, 4)
            starty = round(starty, 4)
            lastx = round(lastx, 4)
            lasty = round(lasty, 4)
            curves.append(
                [
                    (virtual_point.get("x"), virtual_point.get("y")),
                    (lastx, lasty),
                    (startx, starty),
                ]
            )
        if last.get("on") == first.get("on") == "1":
            midx = round(startx + (lastx - startx) / 2, 4)
            midy = round(starty + (lasty - starty) / 2, 4)
            startx = round(startx, 4)
            starty = round(starty, 4)
            lastx = round(lastx, 4)
            lasty = round(lasty, 4)
            curves.append([(startx, starty), (midx, midy), (lastx, lasty)])
    elif len(points) == 2:
        midx = round(startx + (lastx - startx) / 2, 4)
        midy = round(starty + (lasty - starty) / 2, 4)
        startx = round(startx, 4)
        starty = round(starty, 4)
        lastx = round(lastx, 4)
        lasty = round(lasty, 4)
        curves.append([(startx, starty), (midx, midy), (lastx, lasty)])
    return curves


def get_component_contours(component, font_file):
    """
    helper function to gather contours for a glyph that is defined in terms of
    another glyph

    Parameters
    ----------
    component: the XML object for the component tag which corresponds to a
    different glyph

    font_file: XML object of the ttx file for the given font

    Returns
    -------
    all the contours from the component glyph
    """

    glyph_name = component.get("glyph_name")
    glyph = font_file.findall('.//TTGlyph[@name="{}"]'.format(glyph_name))[0]
    return glyph.findall("contour")


def get_contours(glyph, glyph_name, curves, font_file, em_value):
    """
    Given a glyph get all the Bezier curves from each contour

    Parameters
    ----------
    glyph: XML object for glyph

    glyph_name: a string that corresponds to the name of the glyph

    curves: a dictionary in which all of the Bezier curves will be placed

    font_file: XML object of the fontfile, used to pass into get_component_contours

    em_value: size of EM box used for nomalization purposes

    Returns
    -------
    Nothing
    """
    contours = glyph.findall("contour")
    if not contours:
        components = glyph.findall("component")
        for component in components:
            contours = contours + get_component_contours(component, font_file)
    contour_list = []
    for contour in contours:
        contour_list.append(get_curves(contour, em_value))
    curves[glyph_name] = contour_list


def ttx_to_json(file_from, file_to):
    with open(file_from, "r") as f:
        file_string = f.read().encode("ascii", "ignore")

    font_file = cElementTree.fromstring(file_string)
    units_per_em = font_file.findall(".//unitsPerEm")[0]
    em_value = float(units_per_em.get("value"))
    curves = {}
    glyphs = font_file.findall(".//TTGlyph")

    for glyph in glyphs:
        glyph_name = glyph.get("name")
        if glyph_name in CHARACTER_SET:
            get_contours(glyph, glyph_name, curves, font_file, em_value)

    with open(file_to, "w+") as f:
        json.dump(curves, f, sort_keys=True)
