image_filter
============

Image Processing with PIL (Pillow) and cImage

    Originated from assignments in interactivepython.org (Iteration Chapter).
    Applies different filters/algorithms to an image file, displays the changes
    and writes a new file.
    Both PIL and the supplied cImage libraries must be present on your system.
    Get cImage either here or from the original author:
    https://github.com/bnmnetp/cImage
    You can get Pillow here:
    https://pypi.python.org/pypi/Pillow/2.0.0

    Available filters/methods:
    invert - Inverts all pixels in the given image.
    greyscale - Turns picture into a grey version by averaging each pixels RBG values.
    blackwhite - Creates a black and white version of the given image.
    removecolor - Removes one color (currently only red) from the picture.
    sepia - Applies the sepia filter to the given image.
    double - Doubles the size of the image.
    average - Smoothes out the image by averaging the 8 neighbors of a pixel.
    median - Same thing as average but using a median. Likely gives better results.
    
    TODO:
    1. Use colorsys to add HLS, HSV, YIQ compatibility and customization (satu-
    ration, intensity, lightness)
    2. Write testcases
    3. Add file type conversion
    4. Add command line arguments
    5. Add resizing and thumbnail methods
    6. Use gaussian kernel for average() instead of averaging.
        Also source out the neighborhood stuff to a separate method.
    7. Make the write method optional.
