import numpy as np
import pywt
import cv2


def waveletTrans(img, mode='haar', level=1):
    imArray = img

    # Datatype conversions
    # Convert to grayscale
    imArray = cv2.cvtColor(imArray, cv2.COLOR_RGB2GRAY)

    # convert to float
    imArray = np.float32(imArray)
    imArray /= 255

    # compute coefficients
    coeff = pywt.wavedec2(imArray, mode, level=level)

    # Process Coefficients
    coeff_h = list(coeff)
    coeff_h[0] *= 0

    # reconstruction
    imArray_h = pywt.waverec2(coeff_h, mode)
    imArray_h *= 255
    imArray_h = np.uint8(imArray_h)

    return imArray_h