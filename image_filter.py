#!/usr/bin/env python2

""" Image Filter: Image Processing with PIL and cImage

    Originated from assignments in interactivepython.org (Iteration Chapter).
    Applies different filters/algorithms to an image file, displays the changes
    and writes a new file.
    Both PIL and the supplied cImage libraries must be present on your system.

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
    large images as the execution time is O(n) or worse.
    
    TODO:
    1. Use colorsys to add HLS, HSV, YIQ compatibility and customization (satu-
    ration, (r+g+b), lightness)
    2. Write testcases
    3. Add file type conversion
    4. Add command line arguments
    5. Add resizing and thumbnail methods
    6. Use gaussian kernel for average() instead of averaging.
        Also source out the neighborhood stuff to a separate method.
    7. Make the write method optional.
    8. Implement the skip_draw argument properly (per method, not instance).
    9. Fix instance initialisation (make them reusable).
    10. Use empty canvases for everything, skip .copy() for self.newimg.
    11. Empty or 300 lines :o)
"""


import cImage as image
from math import sqrt
from os.path import splitext

class ImageFilter(object):

    def __init__(self, img_file, draw=1):
        "Initialize image, clone it, get its size and create a canvas"
        self.img_file = img_file
        self.oldimg = image.Image(self.img_file)
        self.width = self.oldimg.getWidth()
        self.height = self.oldimg.getHeight()
        self.newimg = self.oldimg.copy()
        # Decides whether to skip drawing the image in a popup window.
        self.draw = draw
        if self.draw:
            self.win = image.ImageWin(self.img_file, self.width, self.height)

    def write(self, func_name="_", draw=1):
        "Draw and save a processed image"
        # Get file's root and extension from method strip_name().
        img_name, img_ext = self.strip_name()
        self.newimg.save(img_name+func_name+img_ext)
        # Again, only execute this if we want to have a popup of the window.
        if self.draw:
            self.newimg.draw(self.win)
            self.win.exitonclick()

    def strip_name(self):
        "Strips the name of a file into (pathname, extension)"
        return splitext(self.img_file)

    def invert(self):
        "Invert the colors of the image"
        for x in range(self.width):
            for y in range(self.height):
                # For each pixel p, get the RGB values and invert them.
                p = self.newimg.getPixel(x,y)
                p.red = 255 - p.red
                p.green = 255 - p.green
                p.blue = 255 - p.blue
                # Write the modified pixel into our cloned window.
                self.newimg.setPixel(x,y,p)
        # Call the method that draws, writes and decides the filename.
        self.write("_inv")

    def greyscale(self):
        "Convert image to greyscale"        
        for x in range(self.width):
            for y in range(self.height):
                # For each pixel p get the RBG values and average them out.
                p = self.newimg.getPixel(x,y)
                avg = (p[0]+p[1]+p[2])/3
                p.red = p.green = p.blue = avg
                self.newimg.setPixel(x,y,p)
        self.write("_grey")

    def blackwhite(self):
        "Convert image to black and white"
        for x in range(self.width):
            for y in range(self.height):
                # Any pixel with an average r+g+b of >= 128 gets converted to
                # white (255), all others to black (0).
                p = self.newimg.getPixel(x,y)
                avg = (p[0]+p[1]+p[2])/3
                if avg >= 128:
                    avg = 255
                else:
                    avg = 0
                p.red = p.green = p.blue = avg
                self.newimg.setPixel(x,y,p)
        self.write("_bw")

    def removecolor(self, color="R"):
        "Remove either (R)ed, (G)reen, (B)lue or a combination of those"
        # TODO: Add options for different colors.
        for x in range(self.width):
            for y in range(self.height):
                p = self.newimg.getPixel(x,y)
                p.red = 0
                self.newimg.setPixel(x,y,p)
        self.write("_rc")
        
    def sepia(self):
        "Apply Sepia Toning to the image"
        for x in range(self.width):
            for y in range(self.height):
                try:
                    # Apply the Sepia filter to each value r, g, b of pixel p.
                    p = self.newimg.getPixel(x,y)
                    p.red = int(p.red * 0.393 + p.green * 0.769 + p.blue * 0.189)
                    p.green = int(p.red * 0.349 + p.green * 0.686 + p.blue * 0.168)
                    p.blue = int(p.red * 0.272 + p.green * 0.534 + p.blue * 0.131)
                    self.newimg.setPixel(x,y,p)
                except:
                    continue
        self.write("_sepia")

    def double(self, draw=0):
        "Double the size of the image"
        # The canvas size gets annoyingly big so by default we avoid drawing here.
        self.draw = draw
        # We overwrite self.newimg because we need double the canvas size.
        self.newimg = image.EmptyImage(self.width*2, self.height*2)
        # In case we do decide to draw, self.win needs double canvas, too.
        if self.draw:
            self.win = image.ImageWin(self.img_file, self.width*2, self.height*2)
    
        for y in range(self.height):
            for x in range(self.width):
                p = self.oldimg.getPixel(x,y)
                self.newimg.setPixel(2*x,2*y, p)
                self.newimg.setPixel(2*x+1, 2*y, p)
                self.newimg.setPixel(2*x, 2*y+1, p)
                self.newimg.setPixel(2*x+1, 2*y+1, p)
        self.write("_double", 0)

    def average(self):
        """Average

        Apply average of surrounding 8 pixels to the current pixel.
        This should probably be updated to use Gaussian instead."""
        
        for y in range(self.height):
            for x in range(self.width):
                # Initialize both pixel p and the list to store neighbor pixels in.
                p = self.newimg.getPixel(x, y)
                neighbors = []
                # Nested for loop to check 9 pixels total: p plus it's 8 neighbors.
                # Use list comprehension here? Also get rid of try statements.
                for xx in range(x-1, x+2):
                    for yy in range(y-1, y+2):
                        try:
                            neighbor = self.newimg.getPixel(xx, yy)
                            neighbors.append(neighbor)
                        except:
                            continue
                nlen = len(neighbors)
                # Average out the RBG values
                if nlen:
                # Uncommented, the following line would leave most of the white 
                # untouched which works a little better for real photographs, imo.
                #~ if nlen and p[0]+p[1]+p[2] < 690:
                    # Get the average of each r, g, b for all pixels in neighbors.
                    p.red = sum([neighbors[i][0] for i in range(nlen)])/nlen
                    p.green = sum([neighbors[i][1] for i in range(nlen)])/nlen
                    p.blue = sum([neighbors[i][2] for i in range(nlen)])/nlen
                    self.newimg.setPixel(x,y,p)
        self.write("_avg")

    def median(self):
        """Median

        Apply median of surrounding 8 pixels to current pixel
        This usually gives better results than average()"""
        
        for y in range(self.height):
            for x in range(self.width):
                # Initialize both pixel p and the list to store neighbor pixels in.
                p = self.newimg.getPixel(x, y)
                neighbors = []
                # Nested for loop to check 9 pixels total: p plus it's 8 neighbors.
                # Use list comprehension here? Also get rid of try statements.
                for xx in range(x-1, x+2):
                    for yy in range(y-1, y+2):
                        try:
                            neighbor = self.newimg.getPixel(xx, yy)
                            neighbors.append(neighbor)
                        except:
                            continue
                nlen = len(neighbors)
                # Making sure the list of pixels is not empty
                if nlen:
                    red = [neighbors[i][0] for i in range(nlen)]
                    green = [neighbors[i][1] for i in range(nlen)]
                    blue = [neighbors[i][2] for i in range(nlen)]
                    # Sort the lists so we can later find the median.
                    for i in [red, green, blue]:
                        i.sort()
                    # If the list has an odd number of items in it, the median is easy.
                    if nlen % 2:
                        p.red = red[len(red)/2]
                        p.green = green[len(green)/2]
                        p.blue = blue[len(blue)/2]
                    # The median calculation if the list length is even:
                    else:
                        p.red = (red[len(red)/2] + red[len(red)/2-1])/2
                        p.green = (green[len(green)/2] + green[len(green)/2-1])/2
                        p.blue = (blue[len(blue)/2] + blue[len(blue)/2-1])/2
                    self.newimg.setPixel(x,y,p)
        self.write("_median")

    def sobel(self, draw=0):
        "Using the Sobel Algorithm to apply Edge Detection to an image."
        self.draw = draw
        # Overwriting self.newimg because we need an empty canvas. Otherwise
        # the existing pixels would influence the newly written ones.
        self.newimg = image.EmptyImage(self.width, self.height)
        if self.draw:
            self.win = image.ImageWin(self.img_file, self.width*2, self.height*2)
            
        # Abandon all hope, ye who enter here. Terrible nested logic incoming.
        for x in range(1, self.width-1):
            for y in range(1, self.height-1):
                # Apply the kx and ky gradient kernels to all pixels.
                kx = ky = 0
                # Nested for loop to check 9 pixels total: p plus it's 8 neighbors.
                # Use list comprehension here? Also get rid of try statements.
                for xx in range(x-1, x+2):
                    for yy in range(y-1, y+2):
                        # Extract RGB of the current neighbor pixel.
                        p = self.oldimg.getPixel(xx, yy)
                        r = p.getRed()
                        g = p.getGreen()
                        b = p.getBlue()

                        ## The actual Sobel algorithm:
                        # Left Row.
                        if xx == x-1:
                            if yy == y-1:
                                kx -= (r+g+b)
                                ky -= (r+g+b)
                            elif yy == y:
                                kx -= 2 * (r+g+b)
                            elif yy == y+1:
                                kx -= (r+g+b)
                                ky += (r+g+b)
                        # Middle Row.
                        elif xx == x and yy == y-1:
                            ky -= 2 * (r+g+b)
                        elif xx == x and yy == y+1:
                            ky += 2 * (r+g+b)
                        # Right Row.
                        elif xx == x+1:
                            if yy == y-1:
                                kx += (r+g+b)
                                ky -= (r+g+b)
                            elif yy == y:
                                kx += 2 * (r+g+b)
                            elif yy == y+1:
                                kx += (r+g+b)
                                ky += (r+g+b)
                # Use Pythagoras' theorem to calc the relative length of kx & ky.
                length = sqrt((kx**2) + (ky**2))
                # Each pixels r+g+b can have 3*255=765 and for +/-4 the maximum is
                # 4*765=3060. The final range is (sqrt(2*3060**2)=4328.
                # Now we can normalize the length to the possible range:
                length = int(length / 4328.0 * 255)

                # Finally, apply the normalized length to each pixel.
                p.red = p.green = p.blue = length
                self.newimg.setPixel(x, y, p)
        self.write("_sobel")


if __name__ == "__main__":
    # Leave out the "draw=0" to produce a popup of the image once it's complete.
    img = ImageFilter("example.png", draw=0)
    img.sobel()
