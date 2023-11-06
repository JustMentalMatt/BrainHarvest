# import tkinter as tk
import customtkinter as tk
from tkinter import filedialog, Canvas
from PIL import Image, ImageTk
from pdf2image import convert_from_path
# from q_pk_IMG import IMG_Cropper - ADD SUPPORT LATER!

class PDF_Cropper:
    def __init__(self, root):
        self.root = root
        self.root.title("question extractor")

        self.canvas = Canvas(root)
        self.canvas.pack(side="left", fill=tk.BOTH, expand=True)

        self.image = None
        self.pdf_paths = []  # multipe file suopoprit
        self.pdf_images = []
        self.page_num = 0
        self.crop_coordinates = None
        self.rect = None

        open_button = tk.CTkButton(root, text="Open File(s)", command=self.open_pdf)
        open_button.pack()
        
        prev_page_button = tk.CTkButton(root, text="Previous Page", command=self.previous_page)
        prev_page_button.pack()
        
        next_page_button = tk.CTkButton(root, text="Next Page", command=self.next_page)
        next_page_button.pack()
        
        crop_button = tk.CTkButton(root, text="Crop Page", command=self.crop_page)
        crop_button.pack()

        self.save_folder = "export_questions"  # dir for da images/ question thinsgys
        self.cropped_image_count = 0

    def open_pdf(self):
        pdf_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf *.PDF")])
        if pdf_paths:
            self.pdf_paths = pdf_paths
            self.pdf_images = self.load_pdf_images(self.pdf_paths)
            self.page_num = 0
            self.show_page()

    def load_pdf_images(self, pdf_paths):
        pdf_images = []
        for pdf_path in pdf_paths:
            pdf_images += convert_from_path(pdf_path, dpi=200)
        return pdf_images
    
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
        self.crop_coordinates = (x1, y1, x1, y1)  # coordinates initilixztion
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
            self.current_cropped_image = self.pdf_images[self.page_num].crop((x1, y1, x2, y2))
            self.crop_coordinates = None
            self.canvas.delete(self.rect)
            self.save_cropped_image()

    def save_cropped_image(self):
        if self.current_cropped_image:
            self.cropped_image_count += 1
            save_path = f"{self.save_folder}/crop_{self.cropped_image_count}.png"
            self.current_cropped_image.save(save_path, "PNG")

    def previous_page(self):
        global page_num
        if self.pdf_images and self.page_num > 0:
            self.page_num -= 1
            self.show_page()
            
    def next_page(self):
        global page_num
        if self.pdf_images and self.page_num < len(self.pdf_images) - 1:
            self.page_num += 1
            print(page_num)
            self.show_page()
            
if __name__ == "__main__":
    root = tk.CTk()
    app = PDF_Cropper(root)
    root.geometry("600x700")  # widnow sisze
    root.mainloop()
