from tkinter import HORIZONTAL

import cv2
import os
import tkinter
from PIL import Image, ImageTk
#                   X   Y
IMAGE_PLACEMENT = [200, 90]
SLIDER_RANGE = 600
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1200
#TODO:
# -image preview creation in init
# -refactor XD XD
# -file explorer
# -video compatibility (how to solve running video? Maybe run videos in different mode - i.e. conver and run on button - dynamic gui)
# -add more filters
# -change to pyqt?
class mainWindow():
    def __init__(self, path):
        self.window = tkinter.Tk()

        self.window.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))
        self.image = cv2.imread(path)
        self.scale_ratio = self.getScaleRatio(shape=self.image.shape)
        self.image_path = path

        self.createGui()
        self.image_preview = tkinter.Label(image=self.opencvToPIL(image=self.image))


    def saveImage(self):
        without_empty_strings = [string for string in self.image_path.split("\\") if string != ""]
        img_name = without_empty_strings[-1]
        base_path = "\\".join(without_empty_strings[:-1])
        base_path = base_path + "\\Canny_" + img_name.split('.')[0]
          
    def createGui(self):
        self.lower_limit = 0
        self.upper_limit = 40

        self.lower_slider = tkinter.Scale(self.window, from_=0, to=SLIDER_RANGE,
                                          orient=HORIZONTAL, variable=self.lower_limit, length=1200,
                                          resolution=1, command=lambda value: self.sliderChange(value))
        self.lower_slider.pack()

        self.upper_slider = tkinter.Scale(self.window, from_=0, to=SLIDER_RANGE, orient=HORIZONTAL,
                                          length=1200, variable=self.upper_limit, resolution=1,
                                          command=lambda value: self.sliderChange(value))
        self.upper_slider.pack()

        # self.button = tkinter.Button(self.window, text="Process photo!",
        #                         command=lambda: self.preparePhotos())
        # self.button.pack()

        # self.canvas = tkinter.Canvas(self.window, width=300, height=300)
        # self.canvas.pack()
        # self.canvas.create_image(20, 20, anchor=tkinter.NW, image=self.image)

        self.window.mainloop()
        self.image_preview.image = self.opencvToPIL(image=self.image)
        self.image_preview.place(x=IMAGE_PLACEMENT[0], y=IMAGE_PLACEMENT[1])

        self.window.update_idletasks()

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
        height, width, _ = self.image.shape
        canny_image = cv2.Canny(self.image, self.lower_slider.get(), self.upper_slider.get())

        canny_image = cv2.resize(canny_image, [int(width * self.scale_ratio), int(height * self.scale_ratio)])
        pil_image = self.opencvToPIL(canny_image)

        self.image_preview = tkinter.Label(image=pil_image)
        self.image_preview.image = pil_image
        self.image_preview.place(x=IMAGE_PLACEMENT[0], y=IMAGE_PLACEMENT[1])
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

        # cv2.imshow("Canny image", canny_image)
        # cv2.waitKey(0)


if __name__ == '__main__':
    # pathh = r'C:\\Users\\gracj\\OneDrive\\Obrazy\\cot.jpg'
    pathh = r'C:\\Users\\gracj\\OneDrive\\Obrazy\\kurczak.jpg'
    window = mainWindow(pathh)
    # cannyImage(pathh)
