import imghdr
import sys
from tkinter import HORIZONTAL

import cv2
import os
import tkinter
from tkinter import filedialog
from tkinter import messagebox as mb
from PIL import Image, ImageTk
from TargetImage import TargetImage

#                   X   Y
IMAGE_PLACEMENT = [200, 120]
SLIDER_RANGE = 600
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1200

IMAGES_EXTENSIONS = "*.jpg* *.jpeg* *.jpe* *.jif* *.jfif* *.jfi* *.gif*"


# TODO:
#  - refactor XD XD XD xd
#  - video compatibility (how to solve running video? Maybe run videos in different mode - i.e. convert and run on button - dynamic gui)
#  - add more filters
#  - change to pyqt?

def opencvToPIL(image):
    """Method that converts photo from opencv array to PIL image instance

        Arguments:
            image - image that is going to be converted

        :return PIL image
    """
    if len(image.shape) > 2:
        b, g, r = cv2.split(image)
        img = cv2.merge((r, g, b))
        im = Image.fromarray(img)
    else:
        im = Image.fromarray(image)

    pil_image = ImageTk.PhotoImage(im)
    return pil_image


def getScaleRatio(shape):
    """ Method calculates image scale to fit into window

        Arguments:
            shape - image shape in opencv array format [height, width, number of channels]
    """
    img_new_height = WINDOW_HEIGHT - IMAGE_PLACEMENT[1]
    height_scale_ratio = img_new_height / shape[0]
    img_new_width = WINDOW_WIDTH - (IMAGE_PLACEMENT[0] * 2)
    width_scale_ratio = img_new_width / shape[1]

    if height_scale_ratio >= width_scale_ratio:
        return width_scale_ratio
    else:
        return height_scale_ratio


class MainWindow:
    def __init__(self):
        self.lower_limit = 0
        self.upper_limit = 40
        self.image_path = None
        self.image = TargetImage()
        self.window = tkinter.Tk()
        self.window.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))
        self.createGui()

    def openExitDialog(self):
        """ Method that calls dialog which closes app or allows to search for photo again """
        if mb.askyesno('No image choosen', 'There is no image/video choosen, do you want to quit?'):
            sys.exit()

    def saveImage(self):
        if self.checkImagePath():
            base_path = self.image_path.split('/')
            file_name = base_path[-1].split(".")
            extension = file_name.pop()

            final_path = "/".join(base_path[:-1]) + "/" + file_name[0] + "_canny." + extension
            
        if self.image.processed is not None:
            cv2.imwrite(final_path, self.image.processed)

    def checkImagePath(self):
        if imghdr.what(self.image_path):
            return True
        else:
            return False

    def browseFiles(self):
        """Method that opens file explorer to choose path of photo"""
        previous_path = self.image_path
        self.image_path = None

        while not self.image_path:
            self.image_path = filedialog.askopenfilename(initialdir="/",
                                                         title="Select a File",
                                                         filetypes=(("Images",
                                                                     IMAGES_EXTENSIONS),
                                                                    ("all files",
                                                                     "*.*")))

            if (self.checkImagePath()) and \
                    (previous_path is not None and previous_path != ''):
                self.image_path = previous_path
                break
            elif not self.checkImagePath():
                self.openExitDialog()
            else:
                self.updatePhoto(self.image_path)

    def updatePhoto(self, update):
        """ Method loads photo selected in GUI if it is different than currently loaded photo
            Arguments:
                update - boolean that tells if photo was updated
        """
        # Show sliders
        self.lower_slider.pack()
        self.upper_slider.pack()

        # Load photo
        self.image(self.image_path)

        # Scale image to fit screen
        scale_ratio = getScaleRatio(shape=self.image.photo.shape)
        self.image.set_scale(scale_ratio)

        # Resize photo to fit window
        resized_image = self.image.resize()

        # Center photo in window
        resized_shape = resized_image.shape
        borders = WINDOW_WIDTH - resized_shape[1]
        IMAGE_PLACEMENT[0] = borders / 2
        self.image_preview.place(x=IMAGE_PLACEMENT[0], y=IMAGE_PLACEMENT[1])

        # Convert cv2 image to PIL
        pil_image = opencvToPIL(image=resized_image)

        # Update image label
        self.image_preview.image = pil_image
        self.image_preview.configure(image=pil_image)
        self.window.update_idletasks()

    def createGui(self):
        """Method creates main window GUI"""
        # Create sliders
        self.lower_slider = tkinter.Scale(self.window, from_=0, to=SLIDER_RANGE,
                                          orient=HORIZONTAL, variable=self.lower_limit, length=1200,
                                          resolution=1, command=lambda value: self.sliderChange())
        self.upper_slider = tkinter.Scale(self.window, from_=0, to=SLIDER_RANGE, orient=HORIZONTAL,
                                          length=1200, variable=self.upper_limit, resolution=1,
                                          command=lambda value: self.sliderChange())

        # Create browser button
        self.search_button = tkinter.Button(self.window, text="Browse files!",
                                            command=lambda: self.browseFiles())
        self.search_button.pack()
        self.search_button = tkinter.Button(self.window, text="Save image!",
                                            command=lambda: self.saveImage())
        self.search_button.pack()

        # Create label image preview
        self.image_preview = tkinter.Label(self.window)
        self.image_preview.pack()

        # Start main window
        self.window.mainloop()

    def sliderChange(self):
        """ Method checks if sliders are set correctly, if not sets them. Then calls image processing"""
        if self.upper_slider.get() <= self.lower_slider.get() <= SLIDER_RANGE - 10:
            self.upper_slider.set(self.lower_slider.get() + 10)
        elif self.upper_slider.get() <= self.lower_slider.get() >= SLIDER_RANGE - 10:
            self.upper_slider.set(SLIDER_RANGE)
        self.convertPhoto()

    # def savePhoto(self, base_path, img_name, image):
    #     """ Method saves image to file
    #         Arguments:
    #             base_path - path where image is located
    #             img_name - image name
    #             image - opencv image array to save
    #     """
    #     print(base_path + "\\" + img_name.split('.')[0] + "1." + img_name.split('.')[1])
    #     cv2.imwrite(base_path + "\\" + img_name.split('.')[0] + "2." + img_name.split('.')[1], image)

    def convertPhoto(self):
        """Method uses canny filter to process photo and update it - on main window
        in futher there will be possibility to use more cv2 filters"""
        pil_image = opencvToPIL(self.image.resize(self.image.canny_filter(self.upper_slider.get(),
                                                                          self.lower_slider.get())))
        # Update image label to show converted photo
        self.image_preview.image = pil_image
        self.image_preview.configure(image=pil_image)
        self.window.update_idletasks()


if __name__ == '__main__':
    window = MainWindow()
