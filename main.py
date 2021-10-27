import sys
from tkinter import HORIZONTAL

import cv2
import os
import tkinter
from tkinter import filedialog
from tkinter import messagebox as mb
from PIL import Image, ImageTk
from ProcessedImage import ProcessedImage

#                   X   Y
IMAGE_PLACEMENT = [200, 120]
SLIDER_RANGE = 600
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1200

IMAGES_EXTENSIONS = "*.jpg* *.jpeg* *.jpe* *.jif* *.jfif* *.jfi*"
# TODO:
# - refactor XD XD XD xd
# - video compatibility (how to solve running video? Maybe run videos in different mode - i.e. conver and run on button - dynamic gui)
# - add more filters
# - change to pyqt?
class mainWindow():
    def __init__(self):
        self.image_path = None
        self.image = ProcessedImage()
        self.window = tkinter.Tk()
        self.window.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))
        self.createGui()

    def openExitDialog(self):
        if mb.askyesno('No image choosen', 'There is no image/video choosen, do you want to quit?'):
            sys.exit()

    def saveImage(self):
        without_empty_strings = [string for string in self.image_path.split("\\") if string != ""]
        img_name = without_empty_strings[-1]
        base_path = "\\".join(without_empty_strings[:-1])
        base_path = base_path + "\\Canny_" + img_name.split('.')[0]

    def browseFiles(self):
        previous_path = self.image_path
        self.image_path = None

        while not self.image_path:
            self.image_path = filedialog.askopenfilename(initialdir="/",
                                                         title="Select a File",
                                                         filetypes=(("Images",
                                                                     IMAGES_EXTENSIONS),
                                                                    ("all files",
                                                                     "*.*")))

            if (self.image_path is None or self.image_path == '') and \
                    (previous_path is not None and previous_path != ''):
                self.image_path = previous_path
                break
            elif self.image_path is False or self.image_path == '':
                self.openExitDialog()

        self.updatePhoto(self.image_path)



    def updatePhoto(self, image):
        if isinstance(image, str) and image != '':
            self.image(image)
        scale_ratio = self.getScaleRatio(shape=self.image.photo.shape)
        self.image.set_scale(scale_ratio)

        # Resize photo to fit window
        resized_image = self.image.resize()

        # Center photo in window
        resized_shape = resized_image.shape
        borders = WINDOW_WIDTH - resized_shape[1]
        IMAGE_PLACEMENT[0] = borders/2
        self.image_preview.place(x=IMAGE_PLACEMENT[0], y=IMAGE_PLACEMENT[1])

        # Convert cv2 image to PIL
        pil_image = self.opencvToPIL(image=resized_image)

        # Update image label
        self.image_preview.image = pil_image
        self.image_preview.configure(image=pil_image)
        self.window.update_idletasks()

    def createGui(self):
        self.lower_limit = 0
        self.upper_limit = 40

        # Create sliders
        self.lower_slider = tkinter.Scale(self.window, from_=0, to=SLIDER_RANGE,
                                          orient=HORIZONTAL, variable=self.lower_limit, length=1200,
                                          resolution=1, command=lambda value: self.sliderChange(value))
        self.lower_slider.pack()

        self.upper_slider = tkinter.Scale(self.window, from_=0, to=SLIDER_RANGE, orient=HORIZONTAL,
                                          length=1200, variable=self.upper_limit, resolution=1,
                                          command=lambda value: self.sliderChange(value))
        self.upper_slider.pack()

        # Create browser button
        self.button = tkinter.Button(self.window, text="Browse files!",
                                     command=lambda: self.browseFiles())
        self.button.pack()

        # Create label image preview
        self.image_preview = tkinter.Label(self.window)
        self.image_preview.pack()

        # Start main window
        self.window.mainloop()

    def sliderChange(self, value):
        if self.upper_slider.get() <= self.lower_slider.get() <= SLIDER_RANGE - 10:
            self.upper_slider.set(self.lower_slider.get() + 10)
        elif self.upper_slider.get() <= self.lower_slider.get() >= SLIDER_RANGE - 10:
            self.upper_slider.set(SLIDER_RANGE)
        self.convertPhoto()

    def savePhoto(self, base_path, img_name, ddd):
        print(base_path + "\\" + img_name.split('.')[0] + "1." + img_name.split('.')[1])
        cv2.imwrite(base_path + "\\" + img_name.split('.')[0] + "2." + img_name.split('.')[1], ddd)

    def opencvToPIL(self, image):
        if len(image.shape) > 2:
            b, g, r = cv2.split(image)
            img = cv2.merge((r, g, b))
            im = Image.fromarray(img)
        else:
            im = Image.fromarray(image)

        pil_image = ImageTk.PhotoImage(im)
        return pil_image

    def convertPhoto(self):
        pil_image = self.opencvToPIL(self.image.resize(self.image.canny_filter(self.upper_slider.get(),
                                                                               self.lower_slider.get())))
        # Update image label to show converted photo
        self.image_preview.image = pil_image
        self.image_preview.configure(image=pil_image)
        self.window.update_idletasks()

    def getScaleRatio(self, shape):
        img_new_height = WINDOW_HEIGHT - IMAGE_PLACEMENT[1]
        height_scale_ratio = img_new_height / shape[0]
        img_new_width = WINDOW_WIDTH - (IMAGE_PLACEMENT[0] * 2)
        width_scale_ratio = img_new_width / shape[1]

        if height_scale_ratio >= width_scale_ratio:
            return width_scale_ratio
        else:
            return height_scale_ratio


if __name__ == '__main__':
    window = mainWindow()
