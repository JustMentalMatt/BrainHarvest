import tkinter as tk
from tkinter import filedialog, Canvas
from PIL import Image, ImageTk

class ImageCroppingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("question extractor")

        self.canvas = Canvas(root)
        self.canvas.pack(side="left", fill=tk.BOTH, expand=True)

        self.image = None
        self.pdf_path = None
        self.pdf_images = []
        self.page_num = 0
        self.crop_coordinates = None
        self.rect = None

        open_button = tk.Button(root, text="Open PDF", command=self.open_pdf)
        open_button.pack()
        
        prev_page_button = tk.Button(root, text="Previous Page", command=self.previous_page)
        prev_page_button.pack()
        
        next_page_button = tk.Button(root, text="Next Page", command=self.next_page)
        next_page_button.pack()

        crop_button = tk.Button(root, text="Crop Page", command=self.crop_page)
        crop_button.pack()

    def open_pdf(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if self.pdf_path:
            self.pdf_images = self.convert_pdf_to_images(self.pdf_path, dpi=200)
            self.page_num = 0
            self.show_page()

    def convert_pdf_to_images(self, pdf_path, dpi=200):
        from pdf2image import convert_from_path
        return convert_from_path(pdf_path, dpi=dpi)
    
    def previous_page(self):
        if self.pdf_images and self.page_num > 0:
            self.page_num -= 1
            self.show_page()
            
    def next_page(self):
        if self.pdf_images and self.page_num < len(self.pdf_images) - 1:
            self.page_num += 1
            self.show_page()

    def show_page(self):
        if self.pdf_images:
            pdf_image = self.pdf_images[self.page_num]
            image = ImageTk.PhotoImage(self.resize_image(pdf_image, self.canvas.winfo_width(), self.canvas.winfo_height()))
            self.image = image
            self.canvas.create_image(0, 0, anchor="nw", image=self.image)

    def resize_image(self, image, width, height):
        return image.resize((width, height), Image.LANCZOS)

    def crop_page(self):
        if self.image:
            self.canvas.bind("<ButtonPress-1>", self.on_press)
            self.canvas.bind("<B1-Motion>", self.on_drag)
            self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        x, y = event.x, event.y
        x1, y1 = self.canvas.canvasx(x), self.canvas.canvasy(y)
        self.crop_coordinates = (x1, y1, x1, y1)  # Initialize with a single point
        self.rect = self.canvas.create_rectangle(x1, y1, x1, y1, outline="red", width=2)

    def on_drag(self, event):
        x, y = event.x, event.y
        x2, y2 = self.canvas.canvasx(x), self.canvas.canvasy(y)
        self.crop_coordinates = (self.crop_coordinates[0], self.crop_coordinates[1], x2, y2)
        self.canvas.coords(self.rect, *self.crop_coordinates)

    def on_release(self, event):
        if self.crop_coordinates:
            x1, y1, x2, y2 = self.crop_coordinates
            page_width, page_height = self.pdf_images[self.page_num].size
            x1, y1, x2, y2 = int(x1 * (page_width / self.canvas.winfo_width())), int(y1 * (page_height / self.canvas.winfo_height())), int(x2 * (page_width / self.canvas.winfo_width())), int(y2 * (page_height / self.canvas.winfo_height()))
            cropped_image = self.pdf_images[self.page_num].crop((x1, y1, x2, y2))
            cropped_image.show()  # You can save this image or do further processing
            self.crop_coordinates = None
            self.canvas.delete(self.rect)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCroppingApp(root)
    root.geometry("600x850")  # Set the initial window size
    root.mainloop()
