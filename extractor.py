import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from pdf2image import convert_from_path

class ImageCroppingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Cropping Tool")

        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        self.image = None
        self.pdf_path = None
        self.pdf_images = []
        self.page_num = 0
        self.crop_coordinates = None
        self.rect = None

        open_button = tk.Button(root, text="Open PDF", command=self.open_pdf)
        open_button.pack()

        next_page_button = tk.Button(root, text="Next Page", command=self.next_page)
        next_page_button.pack()

        crop_button = tk.Button(root, text="Crop Page", command=self.crop_page)
        crop_button.pack()

    def open_pdf(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if self.pdf_path:
            self.pdf_images = convert_from_path(self.pdf_path, dpi=200)
            self.page_num = 0
            self.show_page()

    def next_page(self):
        if self.pdf_images and self.page_num < len(self.pdf_images) - 1:
            self.page_num += 1
            self.show_page()

    def show_page(self):
        if self.pdf_images:
            self.image = ImageTk.PhotoImage(self.pdf_images[self.page_num])
            self.canvas.create_image(0, 0, anchor="nw", image=self.image)
            if self.rect:
                self.canvas.delete(self.rect)

    def crop_page(self):
        if self.image:
            self.canvas.bind("<ButtonPress-1>", self.on_press)
            self.canvas.bind("<B1-Motion>", self.on_drag)
            self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        x, y = event.x, event.y
        self.crop_coordinates = (x, y, x, y)  # Initialize with a single point
        self.rect = self.canvas.create_rectangle(self.crop_coordinates, outline="red")

    def on_drag(self, event):
        x, y = event.x, event.y
        self.crop_coordinates = (self.crop_coordinates[0], self.crop_coordinates[1], x, y)
        self.canvas.coords(self.rect, self.crop_coordinates)

    def on_release(self, event):
        if self.crop_coordinates:
            cropped_image = self.pdf_images[self.page_num].crop(self.crop_coordinates)
            cropped_image.show()  # You can save this image or do further processing
            self.crop_coordinates = None
            self.canvas.delete(self.rect)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCroppingApp(root)
    root.mainloop()
