image-filter
============

Image Processing with PIL (Pillow) and cImage.

    image-filter originated from assignments in interactivepython.org (Iteration Chapter).
    It applies different filters/algorithms to an image file, displays the changes and writes a new file.
    Both the PIL (Pillow) and cImage libraries must be present on your system.

    Available filters/methods:
    invert - Inverts all pixels in the given image.
    greyscale - Turns picture into a grey version by averaging each pixels RBG values.
    blackwhite - Creates a black and white version of the given image.
    removecolor - Removes one color (currently only red) from the picture.
    sepia - Applies the sepia filter to the given image.
    double - Doubles the size of the image.
    average - Smoothes out the image by averaging the 8 neighbors of a pixel.
    median - Same thing as average but using a median. Likely gives better results.
    sobel - Outlines the edges in the picture white, everything else gets dark. Looks cool!

    Please note that this was a learning exercise. Do not use these filters with
    large images as the processing time is O(n) or worse.
