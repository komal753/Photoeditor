import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageEnhance

class PhotoEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Editor")
        self.root.geometry("1000x700")

        # Style and themes
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Left panel for buttons
        self.button_frame = ttk.Frame(self.root, width=200, padding=10)
        self.button_frame.pack(side="left", fill="y")

        # Right panel for the image canvas
        self.image_canvas = tk.Canvas(self.root, bg="#e0e0e0")
        self.image_canvas.pack(side="right", fill="both", expand=True)

        # Backup of the current and original image
        self.current_image = None
        self.original_image = None  # To keep the original image intact for reverting
        self.displayed_image = None  # Image currently displayed on the screen

        self.brightness_value = 1.0
        self.contrast_value = 1.0
        self.resize_factor = 1.0
        self.is_grayscale = False  # Track grayscale state

        # Add buttons with icons and organize them in frames
        self.create_buttons()

    def create_buttons(self):
        button_style = {"padding": 5, "width": 18}

        # Load image button
        self.load_button = ttk.Button(self.button_frame, text="📂 Load Image", command=self.load_image, **button_style)
        self.load_button.pack(pady=5)

        # Resize buttons (increase and decrease)
        self.resize_up_button = ttk.Button(self.button_frame, text="🔍 Increase Size", command=self.increase_size, **button_style)
        self.resize_up_button.pack(pady=5)

        self.resize_down_button = ttk.Button(self.button_frame, text="🔍 Decrease Size", command=self.decrease_size, **button_style)
        self.resize_down_button.pack(pady=5)

        # Rotate buttons (left and right)
        self.rotate_left_button = ttk.Button(self.button_frame, text="↺ Rotate Left", command=self.rotate_left, **button_style)
        self.rotate_left_button.pack(pady=5)

        self.rotate_right_button = ttk.Button(self.button_frame, text="↻ Rotate Right", command=self.rotate_right, **button_style)
        self.rotate_right_button.pack(pady=5)

        # Adjust brightness buttons
        self.brightness_up_button = ttk.Button(self.button_frame, text="☀️ Increase Brightness", command=self.increase_brightness, **button_style)
        self.brightness_up_button.pack(pady=5)

        self.brightness_down_button = ttk.Button(self.button_frame, text="☀️ Decrease Brightness", command=self.decrease_brightness, **button_style)
        self.brightness_down_button.pack(pady=5)

        # Adjust contrast buttons
        self.contrast_up_button = ttk.Button(self.button_frame, text="⚙️ Increase Contrast", command=self.increase_contrast, **button_style)
        self.contrast_up_button.pack(pady=5)

        self.contrast_down_button = ttk.Button(self.button_frame, text="⚙️ Decrease Contrast", command=self.decrease_contrast, **button_style)
        self.contrast_down_button.pack(pady=5)

        # Grayscale button (Toggle)
        self.grayscale_button = ttk.Button(self.button_frame, text="🖤 Grayscale", command=self.toggle_grayscale, **button_style)
        self.grayscale_button.pack(pady=5)

        # Save button
        self.save_button = ttk.Button(self.button_frame, text="💾 Save", command=self.save_image, **button_style)
        self.save_button.pack(pady=5)

    def load_image(self):
        try:
            file_path = filedialog.askopenfilename(
                title="Select an Image",
                filetypes=[
                    ("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),
                    ("All Files", "*.*")
                ]
            )
            if not file_path:
                return

            # Open the image safely
            self.original_image = Image.open(file_path).convert("RGB")
            self.current_image = self.original_image.copy()
            self.displayed_image = self.original_image.copy()

            self.display_image()
            print(f"Image loaded successfully from {file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")
            print(f"Error in load_image: {e}")

    def display_image(self):
        """Display the current image on the canvas."""
        try:
            if self.displayed_image:
                self.image_canvas.delete("all")  # Clear any existing content

                # Resize image to fit canvas if necessary
                canvas_width = self.image_canvas.winfo_width()
                canvas_height = self.image_canvas.winfo_height()
                img_width, img_height = self.displayed_image.size

                self.scale_factor = min(canvas_width / img_width, canvas_height / img_height, 1.0)
                new_width = int(img_width * self.scale_factor)
                new_height = int(img_height * self.scale_factor)

                resized_image = self.displayed_image.resize((new_width, new_height), Image.ANTIALIAS)
                self.img_tk = ImageTk.PhotoImage(resized_image)

                self.image_canvas.create_image(0, 0, anchor="nw", image=self.img_tk)
                self.image_canvas.config(scrollregion=self.image_canvas.bbox("all"))
        except Exception as e:
            messagebox.showerror("Error", f"Error displaying image: {e}")
            print(f"Error displaying image: {e}")

    def increase_brightness(self):
        if self.current_image:
            self.brightness_value += 0.1
            self.apply_brightness()

    def decrease_brightness(self):
        if self.current_image and self.brightness_value > 0.1:
            self.brightness_value -= 0.1
            self.apply_brightness()

    def apply_brightness(self):
        """Apply brightness enhancement on the original image and update the displayed image."""
        if self.current_image:
            enhancer = ImageEnhance.Brightness(self.original_image)
            self.displayed_image = enhancer.enhance(self.brightness_value)
            self.display_image()

    def increase_contrast(self):
        if self.current_image:
            self.contrast_value += 0.1
            self.apply_contrast()

    def decrease_contrast(self):
        if self.current_image and self.contrast_value > 0.1:
            self.contrast_value -= 0.1
            self.apply_contrast()

    def apply_contrast(self):
        """Apply contrast enhancement on the original image and update the displayed image."""
        if self.current_image:
            enhancer = ImageEnhance.Contrast(self.original_image)
            self.displayed_image = enhancer.enhance(self.contrast_value)
            self.display_image()

    def increase_size(self):
        if self.current_image:
            self.resize_factor += 0.1
            self.apply_resize()

    def decrease_size(self):
        if self.current_image and self.resize_factor > 0.1:
            self.resize_factor -= 0.1
            self.apply_resize()

    def apply_resize(self):
        """Apply resizing and update the displayed image."""
        if self.current_image:
            width = int(self.original_image.width * self.resize_factor)
            height = int(self.original_image.height * self.resize_factor)
            self.displayed_image = self.original_image.resize((width, height))
            self.display_image()

    def rotate_left(self):
        if self.current_image:
            self.displayed_image = self.displayed_image.rotate(90, expand=True)  # Rotate left (90 degrees)
            self.display_image()

    def rotate_right(self):
        if self.current_image:
            self.displayed_image = self.displayed_image.rotate(-90, expand=True)  # Rotate right (-90 degrees)
            self.display_image()

    def toggle_grayscale(self):
        """Toggle grayscale on or off."""
        if self.current_image:
            if self.is_grayscale:
                self.displayed_image = self.original_image.copy()
                self.is_grayscale = False
            else:
                self.displayed_image = self.original_image.convert("L")  # Convert to grayscale
                self.is_grayscale = True
            self.display_image()

    def save_image(self):
        """Save the current image to a file."""
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[
                                                         ("PNG files", "*.png"),
                                                         ("JPEG files", "*.jpg"),
                                                         ("All files", "*.*")
                                                     ])
            if not file_path:
                return

            self.displayed_image.save(file_path)
            print(f"Image saved successfully to {file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {e}")
            print(f"Error saving image: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoEditor(root)
    root.mainloop()
