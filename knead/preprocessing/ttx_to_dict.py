from xml.etree import cElementTree
from absl import flags, app
from knead.utils import CHARACTER_SET

FLAGS = flags.FLAGS

flags.DEFINE_string("file", None, "input ttx filename")
flags.mark_flag_as_required("file")


def createPoint(leftPoint, rightPoint, EMvalue):
    """
    create a virtual on-point in-between left and right off-points.

    Parameters
    ----------
    leftPoint : XML object of the left point

    rightPoint: XML object of the right point

    EMvalue: size of EM box used to normalize new point

    Returns
    -------
    New XML object that is the midpoint of left and right points
    """
    leftPointx = int(leftPoint.get("x")) / EMvalue
    rightPointx = int(rightPoint.get("x")) / EMvalue
    newPointx = round(leftPointx + (rightPointx - leftPointx) / 2, 4)
    leftPointy = int(leftPoint.get("y")) / EMvalue
    rightPointy = int(rightPoint.get("y")) / EMvalue
    newPointy = round(leftPointy + (rightPointy - leftPointy) / 2, 4)
    return cElementTree.Element("pt", x=newPointx, y=newPointy, on="1")


def getCurves(contour, EMvalue):
    """
    unpack a contour to all of its Bezier curves

    Parameters
    ----------
    contour: XML object of the contour

    EMvalue : size of EM box, used to normalize points

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
                points = [createPoint(points[0], last_point, EMvalue)] + points
        # now iterate through all the points and build the curves
        loc = 0
        virtualPT = None
        while loc < len(points) - 2:
            currentPT = points[loc]
            nextPT = points[loc + 1]
            twoNextPT = points[loc + 2]
            startx = int(currentPT.get("x")) / EMvalue
            starty = int(currentPT.get("y")) / EMvalue
            nextx = int(nextPT.get("x")) / EMvalue
            nexty = int(nextPT.get("y")) / EMvalue
            lastx = round(int(twoNextPT.get("x")) / EMvalue, 4)
            lasty = round(int(twoNextPT.get("y")) / EMvalue, 4)
            midx = round(startx + (nextx - startx) / 2, 4)
            midy = round(starty + (nexty - starty) / 2, 4)
            startx = round(startx, 4)
            starty = round(starty, 4)
            nextx = round(nextx, 4)
            nexty = round(nexty, 4)
            if virtualPT != None:
                startx = virtualPT.get("x")
                starty = virtualPT.get("y")
                currentPT = virtualPT
                virtualPT = None
            if currentPT.get("on") == nextPT.get("on") == "1":
                curves.append([(startx, starty), (midx, midy), (nextx, nexty)])
                loc += 1
            elif (
                currentPT.get("on") == "1"
                and nextPT.get("on") == "0"
                and twoNextPT.get("on") == "1"
            ):
                curves.append([(startx, starty), (nextx, nexty), (lastx, lasty)])
                loc += 2
            elif (
                currentPT.get("on") == "1"
                and nextPT.get("on") == twoNextPT.get("on") == "0"
            ):
                virtualPT = createPoint(nextPT, twoNextPT, EMvalue)
                curves.append(
                    [
                        (startx, starty),
                        (nextx, nexty),
                        (virtualPT.get("x"), virtualPT.get("y")),
                    ]
                )
                loc += 1
            else:
                raise Exception(
                    "unhandled case",
                    currentPT.get("on"),
                    nextPT.get("on"),
                    twoNextPT.get("on"),
                    virtualPT,
                    currentPT,
                )
    # deal with end cases
    last = points[-1]
    first = points[0]
    startx = int(first.get("x")) / EMvalue
    starty = int(first.get("y")) / EMvalue
    lastx = int(last.get("x")) / EMvalue
    lasty = int(last.get("y")) / EMvalue
    if len(points) > 2:
        secondLast = points[-2]
        secondx = int(secondLast.get("x")) / EMvalue
        secondy = int(secondLast.get("y")) / EMvalue
        if secondLast.get("on") == last.get("on") == "1":
            midx = round(secondx + (lastx - secondx) / 2, 4)
            midy = round(secondy + (lasty - secondy) / 2, 4)
            secondx = round(secondx, 4)
            secondy = round(secondy, 4)
            lastx = round(lastx, 4)
            lasty = round(lasty, 4)
            curves.append([(secondx, secondy), (midx, midy), (lastx, lasty)])
        elif (
            secondLast.get("on") == "1"
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
        elif secondLast.get("on") == last.get("on") == "0" and first.get("on") == "1":
            virtualPT = createPoint(secondLast, last, EMvalue)
            startx = round(startx, 4)
            starty = round(starty, 4)
            lastx = round(lastx, 4)
            lasty = round(lasty, 4)
            curves.append(
                [
                    (virtualPT.get("x"), virtualPT.get("y")),
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


def getCompContour(component, fontFile):
    """
    helper function to gather contours for a glyph that is defined in terms of
    another glyph

    Parameters
    ----------
    component: the XML object for the component tag which corresponds to a
    different glyph

    fontFile: XML object of the ttx file for the given font

    Returns
    -------
    all the contours from the component glyph
    """

    glyphName = component.get("glyphName")
    glyph = fontFile.findall('.//TTGlyph[@name="{}"]'.format(glyphName))[0]
    return glyph.findall("contour")


def getContours(glyph, glyphName, curves, fontFile, EMvalue):
    """
    Given a glyph get all the Bezier curves from each contour

    Parameters
    ----------
    glyph: XML object for glyph

    glyphName: a string that corresponds to the name of the glyph

    curves: a dictionary in which all of the Bezier curves will be placed

    fontFile: XML object of the fontfile, used to pass into getCompContour

    EMvalue: size of EM box used for nomalization purposes

    Returns
    -------
    Nothing
    """
    contours = glyph.findall("contour")
    if not contours:
        components = glyph.findall("component")
        for component in components:
            contours = contours + getCompContour(component, fontFile)
    contourDict = {}
    for i, contour in enumerate(contours):
        c = getCurves(contour, EMvalue)
        contourDict[i] = c
    curves[glyphName] = contourDict


def main(argv):
    fileName = FLAGS.file
    fileObj = open(fileName, "r")
    fileString = fileObj.read().encode("ascii", "ignore")
    fontFile = cElementTree.fromstring(fileString)
    unitEM = fontFile.findall(".//unitsPerEm")[0]
    EMvalue = float(unitEM.get("value"))
    curves = {}
    glyphs = fontFile.findall(".//TTGlyph")
    for glyph in glyphs:
        glyphName = glyph.get("name")
        if glyphName in CHARACTER_SET:
            getContours(glyph, glyphName, curves, fontFile, EMvalue)

    print("{")
    for curve, points in curves.items():
        print(repr(curve), ":", points, ",")
    print("}")


if __name__ == "__main__":
    app.run(main)
