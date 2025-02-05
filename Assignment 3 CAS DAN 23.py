import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import *
from PIL import Image, ImageTk
import numpy as np


class EnhancedImageProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("IMAGE EDITOR APP")
        self.root.geometry("1000x600")
        self.root.configure(bg="light green")  # Light blue theme

        # Initialize image attributes
        self.original_image = None
        self.modified_image = None
        self.current_image = None
        self.history = []
        self.selection_rect = None
        self.start_x = self.start_y = None
        self.crop_mode = False
        self.cropped_image = None
        self.original_cropped_image = None  # Store the original cropped image
        self.rect_start = None
        self.rect_end = None
        self.crop_rect_id = None
        self.undo_stack = []
        self.redo_stack = []

        # Modern UI Elements
        self.create_gui()
        self.add_shortcuts()

    def create_gui(self):
        # Main container
        frame = Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Image canvases
        self.canvas_frame = Frame(frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        self.original_canvas = tk.Canvas(self.canvas_frame, width=500, height=450)
        self.original_canvas.pack(side=tk.LEFT, padx=10, pady=10)

        self.modified_canvas = tk.Canvas(self.canvas_frame, width=500, height=450)                             
        self.modified_canvas.pack(side=tk.RIGHT, padx=10, pady=10)

        # Control panel
        control_frame = Frame(frame, bg='dark grey', pady=10)
        control_frame.pack(fill=tk.X)

        load_image = Button(control_frame, text="Load Image", command=self.load_image)
        load_image.pack(side=tk.LEFT, padx=10)

        save_image_button = Button(control_frame, text="Save Image", command=self.save_image)
        save_image_button.pack(side=tk.LEFT, padx=10)

        undo_button = Button(control_frame, text="Undo Changes", command=self.undo)
        undo_button.pack(side=tk.LEFT, padx=10)

        redo_button = Button(control_frame, text="Redo Changes", command=self.redo)
        redo_button.pack(side=tk.LEFT, padx=10)

        crop_button = Button(control_frame, text="Crop Image", command=self.toggle_crop_mode)
        crop_button.pack(side=tk.LEFT, padx=10)

        gray_button = Button(control_frame, text="Grayscale Image", command=self.apply_grayscale)
        gray_button.pack(side=tk.LEFT, padx=10)

        rotate_button = Button(control_frame, text="Rotate Image", command=self.rotate_image)
        rotate_button.pack(side=tk.LEFT, padx=10)

        blur_button=Button(control_frame,text="Blur Image",command=self.blur_image)
        blur_button.pack(side=tk.LEFT,padx=10)

        edge_button=Button(control_frame,text="Edge Detection",command=self.edge_detection)
        edge_button.pack(side=tk.LEFT,padx=10)



        # Resize slider with modern styling
        self.resize_scale = Scale(control_frame, label="Image Resize", from_=10, to=200, orient=tk.HORIZONTAL)
        self.resize_scale.pack(side=tk.LEFT, padx=10)
        self.resize_scale.set(100)
        self.resize_scale.bind("<Motion>", self.preview_resize)

    def add_shortcuts(self):
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.root.bind("<Control-y>", lambda e: self.redo())
        self.root.bind("<Control-s>", lambda e: self.save_image())

    def toggle_crop_mode(self):
        self.crop_mode = not self.crop_mode
        if self.crop_mode:
            self.modified_canvas.bind("<ButtonPress-1>", self.start_crop)
            self.modified_canvas.bind("<B1-Motion>", self.update_crop)
            self.modified_canvas.bind("<ButtonRelease-1>", self.finalize_crop)
        else:
            self.modified_canvas.unbind("<ButtonPress-1>")
            self.modified_canvas.unbind("<B1-Motion>")
            self.modified_canvas.unbind("<ButtonRelease-1>")

    def start_crop(self, event):
        self.rect_start = (event.x, event.y)

    def update_crop(self, event):
        if self.crop_rect_id:
            self.modified_canvas.delete(self.crop_rect_id)
        self.rect_end = (event.x, event.y)
        self.crop_rect_id = self.modified_canvas.create_rectangle(
            self.rect_start[0], self.rect_start[1], event.x, event.y, outline="red", dash=(4, 2)
        )

    def finalize_crop(self, event):
        if self.modified_image is None:
            return

        x1, y1 = self.rect_start
        x2, y2 = self.rect_end
        x1, x2 = sorted((x1, x2))
        y1, y2 = sorted((y1, y2))

        h, w, _ = self.modified_image.shape
        scale_x = w / 500
        scale_y = h / 400

        x1, x2 = int(x1 * scale_x), int(x2 * scale_x)
        y1, y2 = int(y1 * scale_y), int(y2 * scale_y)

        self.cropped_image = self.modified_image[y1:y2, x1:x2].copy()
        self.modified_image = self.cropped_image.copy()  # Update the modified image
        self.show_images()
         # If you have a save button in your GUI, enable it
        self.update_history()

    def preview_resize(self, event):
        if self.modified_image is not None:
            quality = self.resize_scale.get() / 100.0
            h, w = self.modified_image.shape[:2]
            new_w = int(w * quality)
            new_h = int(h * quality)
            resized = cv2.resize(self.modified_image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
            self.update_modified_preview(resized)

    def update_modified_preview(self, image):
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img.thumbnail((500, 450))
        self.modified_photo = ImageTk.PhotoImage(img)
        self.modified_canvas.create_image(0, 0, anchor=tk.NW, image=self.modified_photo)

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return
        try:
            self.original_image = cv2.imread(file_path)
            if self.original_image is None:
                raise ValueError("Invalid image file")
            self.current_image = self.original_image.copy()
            self.modified_image = self.current_image.copy()
            self.history = [self.current_image.copy()]
            self.redo_stack = []
            self.show_images()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image:\n{str(e)}")

    def show_images(self):
        # Show original image
        if self.original_image is not None:
            orig_img = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
            orig_img = Image.fromarray(orig_img)
            orig_img.thumbnail((500, 500))
            self.original_photo = ImageTk.PhotoImage(orig_img)
            self.original_canvas.create_image(0, 0, anchor=tk.NW, image=self.original_photo)

        # Show modified image
        if self.modified_image is not None:
            mod_img = cv2.cvtColor(self.modified_image, cv2.COLOR_BGR2RGB)
            mod_img = Image.fromarray(mod_img)
            mod_img.thumbnail((500, 500))
            self.modified_photo = ImageTk.PhotoImage(mod_img)
            self.modified_canvas.create_image(0, 0, anchor=tk.NW, image=self.modified_photo)

    def save_image(self):
        if self.modified_image is not None:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")]
            )
            if file_path:
                cv2.imwrite(file_path, self.modified_image)
                messagebox.showinfo("Success", "Image saved successfully!")

    def update_history(self):
        self.history.append(self.modified_image.copy())
        self.redo_stack = []

    def undo(self):
        if len(self.history) > 1:
            self.redo_stack.append(self.history.pop())
            self.modified_image = self.history[-1].copy()
            self.show_images()

    def redo(self):
        if self.redo_stack:
            self.history.append(self.redo_stack.pop())
            self.modified_image = self.history[-1].copy()
            self.show_images()

    def apply_grayscale(self):
        if self.modified_image is not None:
            self.update_history()
            gray = cv2.cvtColor(self.modified_image, cv2.COLOR_BGR2GRAY)
            self.modified_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            self.show_images()

    def rotate_image(self):
        if self.modified_image is not None:
            self.update_history()
            self.modified_image = cv2.rotate(self.modified_image, cv2.ROTATE_90_CLOCKWISE)
            self.show_images()
    
    def blur_image(self):
       if self.modified_image is not None:
          self.update_history()
        # Apply Gaussian blur with a kernel size of (15, 15)
          self.modified_image = cv2.GaussianBlur(self.modified_image, (15, 15), 0)
          self.show_images()

    def edge_detection(self):
       if self.modified_image is not None:
          self.update_history()
        # Convert to grayscale first
          gray_image = cv2.cvtColor(self.modified_image, cv2.COLOR_BGR2GRAY)
        # Apply Canny edge detection
          edges = cv2.Canny(gray_image, 100, 200)
        # Convert back to 3 channels (BGR)
          self.modified_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
          self.show_images()

if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedImageProcessor(root)
    root.mainloop()

