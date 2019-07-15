#!/usr/bin/env python3
import numpy as np


def clip_result(func):
    ''' decorator to ensure result in limits 0..1 '''
    def wrapper(*args, **kwargs):
        y = func(*args, **kwargs)
        y = np.clip(y, 0, 1)
        return y
    return wrapper


def invert(y):
    return 1 - y


def mirror(y):
    return np.flip(y, 1)


def flip(y):
    return np.flip(y, 0)


@clip_result
def normalize(y):
    ''' Normalize array --> values 0...1 '''
    return (y - y.min()) / y.ptp()


@clip_result
def equalize(y):
    from skimage import exposure
    return exposure.equalize_hist(y)


@clip_result
def adaptive_equalize(y, clip_limit=0.03):
    from skimage import exposure
    return exposure.equalize_adapthist(y, clip_limit=clip_limit)


@clip_result
def gamma(y, g):
    """gamma correction of an numpy float image, where
    g = 1 ~ no effect, g > 1 ~ darken, g < 1 ~ brighten
    """
    return y ** g


@clip_result
def unsharp_mask(y, radius, amount):
    from scipy.ndimage import gaussian_filter
    mask = gaussian_filter(y, radius)
    y = y + amount * (y - mask)
    return y


@clip_result
def blur(y, radius=3):
    from scipy.ndimage import gaussian_filter
    return gaussian_filter(y, radius)


@clip_result
def contrast(y, f):
    """ change contrast """
    return .5 + f * (y - .5)


@clip_result
def multiply(y, f):
    """ multiply by scalar """
    return y * f


@clip_result
def fill(y, f=1):
    """ change to constant """
    return f


@clip_result
def add(y, f):
    """ change brightness """
    return y + f


def tres_high(y, f):
    """  change value of light pixels to 1 """
    y[y > f] = 1
    return y


def tres_low(y, f):
    """ change value of dark pixels to 0 """
    y[y < f] = 0
    return y


def clip_high(y, f):
    """ change value of light pixels to limit """
    y[y > f] = f
    return y


def clip_low(y, f):
    """ change value of dark pixels to limit """
    y[y < f] = f
    return y


@clip_result
def sigma(y, sigma=2):
    """ s shaped curve """
    y = np.tanh((y - .5) * sigma) / 2 + .5
    return y


def fft(y):
    from scipy import fftpack
    # Take the fourier transform of the image.
    y = y * 255
    F1 = fftpack.fft2(y)
    # Now shift the quadrants around so that low spatial frequencies are in
    # the center of the 2D fourier transformed image.
    F2 = np.fft.fftshift(F1).real
    ftimage = np.abs(F2)
    ftimage = np.log(ftimage)
    return ftimage


def ifft(y):
    F2 = np.exp(y)
    F1 = np.fft.ifftshift(F2)
    img = np.fft.ifft2(F1).real
    img = img / 255
    return img


@clip_result
def high_pass(y, sigma):
    from scipy.ndimage import gaussian_filter
    bg = gaussian_filter(y, sigma=sigma)
    y = y - bg
    return y
