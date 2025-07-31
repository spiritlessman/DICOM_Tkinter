import tkinter as tk
from tkinter import filedialog, Text
import pydicom
from PIL import Image, ImageTk
import numpy as np
from numpy.typing import NDArray

def open_dicom():
    file_path = filedialog.askopenfilename(initialdir=".", filetypes=[("DICOM files", "*.dcm")])
    if not file_path:
        return

    root.after(100, lambda: load_dicom(file_path))

def load_dicom(file_path: str):
    # Read DICOM
    ds = pydicom.dcmread(file_path)
    # Print header
    text_box.delete("1.0", tk.END)
    for idx, elem in enumerate(ds):
        if idx == 100:
            break
        if elem.keyword:
            text_box.insert(tk.END, f"{elem.keyword}: {elem.value}\n")

    # Image pixel data
    if 'PixelData' in ds:
        pixel_array = ds.pixel_array[int(ds.pixel_array.shape[0] / 2)] if ds.pixel_array.ndim == 3 else ds.pixel_array
        image = Image.fromarray(normalize_pixel_array(pixel_array))
        # image = image.resize((256, 256))
        photo = ImageTk.PhotoImage(image)

        image_label.config(image=photo)
        image_label.image = photo

def normalize_pixel_array(arr: NDArray):
    arr = arr.astype(np.float32)
    arr = (arr - arr.min()) / (arr.max() - arr.min()) * 255.0
    return arr.astype(np.uint8)

# Initialize GUI.
root = tk.Tk()
root.title("Simple DICOM Viewer")
root.geometry("800x600")

canvas = tk.Canvas(root)
canvas.pack(side="left", fill="both", expand=True)

# Connect vertical scroll bar.
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame in the canvas.
scrollable_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", on_configure)

# Make a button to open DICOM.
open_btn = tk.Button(scrollable_frame, text="Open DICOM", command=open_dicom)
open_btn.pack()

# The area for printing image
image_label = tk.Label(scrollable_frame)
image_label.pack(pady=10)

# Text box for header
text_box = Text(scrollable_frame, height=20, width=100)
text_box.pack()

root.mainloop()