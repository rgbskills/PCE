import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter
import numpy as np
from sklearn.cluster import KMeans

# Adjust this limit if necessary, or set it to None to remove the limit
Image.MAX_IMAGE_PIXELS = None

def extract_primary_colors(image_path, num_colors=3):
    # Load image and convert to RGB
    image = Image.open(image_path).convert('RGB')
    image = image.resize((150, 150))  # Resize for faster processing
    np_image = np.array(image)

    # Reshape image data for KMeans
    np_image = np_image.reshape((np_image.shape[0] * np_image.shape[1], 3))

    # Apply KMeans to find primary colors (explicitly set n_init)
    kmeans = KMeans(n_clusters=num_colors, n_init=10)
    kmeans.fit(np_image)

    # Extract the colors
    colors = kmeans.cluster_centers_
    return colors.astype(int)

def copy_to_clipboard(text):
    try:
        pyperclip.copy(text)
        messagebox.showinfo("Copied", f"Copied to clipboard: {text}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def create_color_widgets(color, parent):
    color_hex = f'#{int(color[0]):02x}{int(color[1]):02x}{int(color[2]):02x}'
    color_rgb = f'rgb({int(color[0])}, {int(color[1])}, {int(color[2])})'

    frame = tk.Frame(parent, bg=color_hex)
    frame.pack(padx=5, pady=5)

    color_label = tk.Label(frame, bg=color_hex, width=20, height=2)
    color_label.pack(side=tk.LEFT, padx=5)

    copy_hex_btn = tk.Button(frame, text="Copy Hex", command=lambda: copy_to_clipboard(color_hex))
    copy_hex_btn.pack(side=tk.LEFT, padx=5)

    copy_rgb_btn = tk.Button(frame, text="Copy CSS RGB", command=lambda: copy_to_clipboard(color_rgb))
    copy_rgb_btn.pack(side=tk.LEFT, padx=5)

def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        # Extract colors
        colors = extract_primary_colors(file_path)

        # Display image
        img = Image.open(file_path)
        img = img.resize((250, 250), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        panel.configure(image=img)
        panel.image = img

        # Clear existing color frames (if any)
        for frame in color_frame.winfo_children():
            frame.destroy()

        # Create color frames with labels and copy buttons
        for color in colors:
            create_color_widgets(color, color_frame)

window = tk.Tk()
window.title("Image Color Extractor")

# Frame for image
frame = tk.Frame(window)
frame.pack()

# Button to open image
open_button = tk.Button(frame, text='Open Image', command=open_image)
open_button.pack()

# Panel to display image
panel = tk.Label(frame)
panel.pack()

# Frame for color labels
color_frame = tk.Frame(window)
color_frame.pack()

window.mainloop()
