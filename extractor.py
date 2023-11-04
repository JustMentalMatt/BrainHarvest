import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageCroppingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Cropping Tool")

        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        self.image = None
        self.image_path = None
        self.crop_coordinates = None
        self.rect = None

        open_button = tk.Button(root, text="Open Image", command=self.open_image)
        open_button.pack()

        crop_button = tk.Button(root, text="Crop Image", command=self.crop_image)
        crop_button.pack()

    def open_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ppm *.pgm *.PDF")])
        if self.image_path:
            image = Image.open(self.image_path)
            self.image = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.image)

    def crop_image(self):
        if self.image_path:
            self.canvas.bind("<ButtonPress-1>", self.on_press)
            self.canvas.bind("<B1-Motion>", self.on_drag)
            self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        x, y = event.x, event.y
        self.crop_coordinates = (x, y, x, y)
        self.rect = self.canvas.create_rectangle(self.crop_coordinates, outline="red")

    def on_drag(self, event):
        x, y = event.x, event.y
        self.crop_coordinates = (self.crop_coordinates[0], self.crop_coordinates[1], x, y)
        self.canvas.coords(self.rect, self.crop_coordinates)

    def on_release(self, event):
        if self.crop_coordinates:
            cropped_image = Image.open(self.image_path).crop(self.crop_coordinates)
            cropped_image.show()  # You can save this image or do further processing
            self.crop_coordinates = None
            self.canvas.delete(self.rect)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCroppingApp(root)
    root.mainloop()
