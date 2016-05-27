
import imutils
import cv2
import numpy as np

from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import cv2

class ColorLabeler:
    def __init__(self):
        # init the colors dict, containing the color name and RGB value
        colors = OrderedDict({'red': (255, 0, 0), 'green': (0, 255, 0), 'blue': (0, 0, 255)})

        # allocate memory for the L*a*b* image, then init the color names list
        self.lab = np.zeros((len(colors), 1, 3), dtype='uint8')
        self.colorNames = []

        # loop over the colors dict
        for (i, (name, rgb)) in enumerate(colors.items()):
            # update the L*a*b* array and the color names list
            self.lab[i] = rgb
            self.colorNames.append(name)

        # convert the L*a*b* array from the RGB color space to L*a*b*
        self.lab = cv2.cvtColor(self.lab, cv2.COLOR_RGB2LAB)

    def label(self, image, c):

        # construct a mask for the contour, then compute the
        # average L*a*b* value for the masked region
        mask = np.zeros(image.shape[:2], dtype='uint8')
        cv2.drawContours(mask, [c], -1, 255, -1)
        mask = cv2.erode(mask, None, iterations=2)
        mean = cv2.mean(image, mask=mask)[:3]

        # init the min distance found thus far
        minDist = (np.inf, None)

        # loop over the known L*a*b* color values
        for (i, row) in enumerate(self.lab):
            # compute the distance between the current L*a*b*
            # color value and the mean of the image
            d = dist.euclidean(row[0], mean)

            # if the distance is smaller than the current distance
            # then update the bookkeeping variable
            if d < minDist[0]:
                minDist = (d, i)

        # return the name of the color with the smallest distance
        return self.colorNames[minDist[1]]

class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c):
        # init the shape name and approximate the contour

        shape = 'unidentified'
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.03 * peri, True)

        # if the shape is a triangle, it will have 3 vertices
        if len(approx) <= 6:
            shape = 'shell'

        # if the shape has 4, it is a square or rectangle
        elif len(approx) >= 10:
            shape = 'star'

        # else assume it's a circle
        else:
            shape = 'circle'

        return shape

def detect_color():

    new_graph = [[[] for _ in range(9)] for _ in range(9)]
    # load the image and resize it to a smaller factor
    # so that the shapes can be approximated better

    my_image = 'bc_myedit.jpg'
    #my_image = 'untitled.png'

    image = cv2.imread(my_image)

    # blur the resized image slightly, then convert it to both
    # graysale and the L*a*b* color spaces

    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
    binary = cv2.bitwise_not(thresh)

    # find contours in the thresholded image
    cnts = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    # make copy of image
    image_copy = np.copy(image)

    # find contours of large enough area
    min_cnt_area = 750
    large_cnts = [cnt for cnt in cnts if cv2.contourArea(cnt) > min_cnt_area]

    # draw contours
    cv2.drawContours(image_copy, large_cnts, -1, (255,0,0))


    # init
    sd = ShapeDetector()
    cl = ColorLabeler()

    # loop over cnts

    for c in large_cnts:

        # compute the center of the contour

        M = cv2.moments(c)
        try:
            cX = int((M['m10'] / M['m00']))
            cY = int((M['m01'] / M['m00']))
        except:
            cX = 0
            cY = 0

        # detect the shape of the contour and label the color

        shape = sd.detect(c)
        color = cl.label(lab, c)

        # multiply the contour (x, y) coords by the resize ratio,
        # then draw the contours and the name of the shape and labeled
        # color on the image

        c = c.astype('float')
        c = c.astype('int')
        text = '{} {}'.format(color, shape)
        cv2.drawContours(image, [c], -1, (0, 0, 0), 2)
        cv2.putText(image, text, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 2)

        y_graph = int(round(cX / 80))
        x_graph = int(round(cY / 80))
        new_graph[x_graph][y_graph] = [color, shape]

        # show image

        #cv2.imshow('image', image)
        #cv2.waitKey(0)

    return new_graph

#detect_color()
