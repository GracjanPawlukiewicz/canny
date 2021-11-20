import imghdr
import sys
from tkinter import HORIZONTAL

import cv2
import os
import tkinter
from tkinter import filedialog
from tkinter import messagebox as mb
from TargetImage import TargetImage
from utils import opencvToPIL, getScaleRatio

SLIDER_RANGE = 600
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1200

IMAGES_EXTENSIONS = "*.jpg* *.jpeg* *.jpe* *.jif* *.jfif* *.jfi* *.gif*"


# TODO:
#  - refactor XD XD XD xd
#  - video compatibility (how to solve running video? Maybe run videos in different mode - i.e. convert and run on button - dynamic gui)
#  - add more filters
#  - change to pyqt?


class MainWindow:
    def __init__(self):
        self.lower_limit = 0
        self.upper_limit = 40
        #                        X    Y
        self.image_placement = [200, 160]

        self.image_path = None
        self.image = TargetImage()
        self.window = tkinter.Tk()
        self.window.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))
        self.createGui()

    def openExitDialog(self):
        """ Method that calls dialog which closes app or allows to search for photo again """
        if mb.askyesno('No image choosen', 'There is no image/video choosen, do you want to quit?'):
            sys.exit()

    def openWarningDialog(self, warning):
        """ Method that calls warning dialog when there is no image processed"""

        mb.showwarning('No image processed', 'There is nothing to save!\n' + warning)

    def checkImagePath(self):
        try:
            if imghdr.what(self.image_path):
                return True
            else:
                return False
        except AttributeError:
            self.openWarningDialog("No path selected!")

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
                self.updatePreview(self.image_path)

    def updatePreview(self, update):
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
        scale_ratio = getScaleRatio(shape=self.image.photo.shape, width=WINDOW_WIDTH,
                                    height=WINDOW_HEIGHT, image_placement=self.image_placement)
        self.image.setScale(scale_ratio)

        # Resize photo to fit window
        resized_image = self.image.resize_image()

        # Center photo in window
        resized_shape = resized_image.shape
        borders = WINDOW_WIDTH - resized_shape[1]
        self.image_placement[0] = borders / 2
        self.image_preview.place(x=self.image_placement[0], y=self.image_placement[1])

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

    def convertPhoto(self):
        """Method uses canny filter to process photo and update it - on main window
        in futher there will be possibility to use more cv2 filters"""
        pil_image = opencvToPIL(self.image.resize_image(self.image.canny_filter(self.upper_slider.get(),
                                                                                self.lower_slider.get())))
        # Update image label to show converted photo
        self.image_preview.image = pil_image
        self.image_preview.configure(image=pil_image)
        self.window.update_idletasks()


if __name__ == '__main__':
    window = MainWindow()
