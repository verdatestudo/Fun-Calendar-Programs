'''
Detect Color and Shape BC
Helper for Beach Combing - Calendar Problem Solver
Detects color and shape of tiles in puzzle

First Created: 2016-May-26
Last Updated: 2016-May-28
Python 2.7
Chris

See beach_combing_puzzle.png
'''

from PIL import ImageEnhance
from scipy.spatial import distance as dist
from collections import OrderedDict
import imutils
import numpy as np
import cv2

from skimage import data, img_as_float
from skimage import exposure
from skimage import io

class ColorLabeler:
    '''
    Takes a shape/contourgroup in an image and returns the nearest color (Euclidean distance).
    '''
    def __init__(self):
        # init the colors dict, containing the color name and RGB value
        colors = OrderedDict({'red': (255, 0, 0), 'green': (0, 255, 0), 'blue': (0, 0, 255)})

        # allocate memory for the L*a*b* image, then init the color names list
        self.lab = np.zeros((len(colors), 1, 3), dtype='uint8')
        self.color_names = []

        # loop over the colors dict
        for (i, (name, rgb)) in enumerate(colors.items()):
            # update the L*a*b* array and the color names list
            self.lab[i] = rgb
            self.color_names.append(name)

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
        return self.color_names[minDist[1]]

class ShapeDetector:
    '''
    Takes a shape/contourgroup and returns the nearest shape based on rules set in this class.
    '''
    def __init__(self):
        pass

    def detect(self, c):
        # init the shape name and approximate the contour

        shape = 'unidentified'
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.03 * peri, True)

        if len(approx) <= 6:
            shape = 'shell'
        elif len(approx) >= 10:
            shape = 'star'
        else:
            shape = 'circle'

        return shape

def image_equalization(image_file):
    '''
    in testing
    '''
    # Load an example image
    img = io.imread(image_file)
    #img = data.moon()
    #img = 'new.jpg'

    # Contrast stretching
    p2, p98 = np.percentile(img, (2, 98))
    img_rescale = exposure.rescale_intensity(img, in_range=(p2, p98))

    img_rescale = exposure.adjust_sigmoid(img_rescale, 0.5, 5)

    # Equalization
    img_eq = exposure.equalize_hist(img)

    # Adaptive Equalization
    img_adapteq = exposure.equalize_adapthist(img, clip_limit=0.03)

    '''
    cv2.imshow('image', img)
    cv2.waitKey(0)
    '''

    cv2.imshow('image', img_rescale)
    cv2.waitKey(0)

    '''
    cv2.imshow('image', img_eq)
    cv2.waitKey(0)
    cv2.imshow('image', img_adapteq)
    cv2.waitKey(0)
    '''

    cv2.imwrite('new_adj.jpg', img_rescale)
    '''
    cv2.imwrite('new_adj2.jpg', img_eq)
    cv2.imwrite('new_adj3.jpg', img_adapteq)
    '''

    return ['new_adj.jpg', 1, 2] #'new_adj2.jpg', 'new_adj3.jpg']


def detect_color_and_shape(image_file):
    '''
    Finds the shape and color of each tile in the puzzle.
    Returns these values in a 2d list.
    '''

    new_graph = [[[] for _ in range(9)] for _ in range(9)]

    #my_image = 'bc_myedit.jpg'
    image = cv2.imread(image_file)

    # blur the resized image slightly, then convert it to both
    # graysale and the L*a*b* color space

    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
    binary = cv2.bitwise_not(thresh)

    cv2.imshow('image', binary)
    cv2.waitKey(0)

    # find contours in the thresholded image
    cnts = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    # make copy of image
    image_copy = np.copy(image)

    # find contours of large enough area
    min_cnt_area = 750
    large_cnts = [cnt for cnt in cnts if cv2.contourArea(cnt) > min_cnt_area]

    # draw contours
    cv2.drawContours(image_copy, large_cnts, -1, (255, 0, 0))

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

        # draw the contours and the name of the shape and labeled
        # color on the image

        c = c.astype('float')
        c = c.astype('int')
        txt_color = color
        txt_shape = shape
        #text = '{} {}'.format(color, shape)
        cv2.drawContours(image, [c], -1, (0, 0, 0), 2)
        cv2.putText(image, txt_color, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        cv2.putText(image, txt_shape, (cX, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        y_graph = int(round(cX / 80))
        x_graph = int(round(cY / 80))
        new_graph[x_graph][y_graph] = [color, shape]

    # show image

    cv2.imshow('image', image)
    cv2.waitKey(0)

    return new_graph

#detect_color_and_shape('bc_myedit.jpg')
