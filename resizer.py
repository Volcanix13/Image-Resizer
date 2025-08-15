import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

# -------------------
# Textes multilingues
# -------------------
TEXTS = {
    "FR": {
        "title": "Redimensionneur d'images",
        "select_img": "Sélectionner une image",
        "width": "Largeur (px)",
        "height": "Hauteur (px)",
        "keep_ratio": "Conserver les proportions",
        "resize": "Redimensionner",
        "success": "Image redimensionnée avec succès !",
        "error": "Erreur lors du redimensionnement."
    },
    "EN": {
        "title": "Image Resizer",
        "select_img": "Select an image",
        "width": "Width (px)",
        "height": "Height (px)",
        "keep_ratio": "Keep aspect ratio",
        "resize": "Resize",
        "success": "Image resized successfully!",
        "error": "Error while resizing."
    }
}

# -------------------
# Variables globales
# -------------------
lang = "FR"
img_path = None
original_img = None

# -------------------
# Fonctions
# -------------------
def update_language():
    global lang
    lang = lang_var.get()
    t = TEXTS[lang]
    root.title(t["title"])
    btn_select.config(text=t["select_img"])
    lbl_width.config(text=t["width"])
    lbl_height.config(text=t["height"])
    chk_keep_ratio.config(text=t["keep_ratio"])
    btn_resize.config(text=t["resize"])

def select_image():
    global img_path, original_img
    img_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif")])
    if img_path:
        original_img = Image.open(img_path)
        entry_width.delete(0, tk.END)
        entry_height.delete(0, tk.END)
        entry_width.insert(0, original_img.width)
        entry_height.insert(0, original_img.height)

def resize_image():
    try:
        if not img_path:
            return
        width = int(entry_width.get())
        height = int(entry_height.get())

        img = original_img.copy()
        if keep_ratio_var.get():
            img.thumbnail((width, height))
        else:
            img = img.resize((width, height))

        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("All Files", "*.*")])
        if save_path:
            img.save(save_path)
            messagebox.showinfo(TEXTS[lang]["title"], TEXTS[lang]["success"])
    except Exception as e:
        messagebox.showerror(TEXTS[lang]["title"], f"{TEXTS[lang]['error']}\n{e}")

# -------------------
# Interface graphique
# -------------------
root = tk.Tk()
root.geometry("320x220")

# Sélecteur de langue
lang_var = tk.StringVar(value=lang)
lang_menu = tk.OptionMenu(root, lang_var, "FR", "EN", command=lambda _: update_language())
lang_menu.pack(pady=5)

frame = tk.Frame(root)
frame.pack(pady=5)

btn_select = tk.Button(frame, command=select_image)
btn_select.grid(row=0, column=0, columnspan=2, pady=5)

lbl_width = tk.Label(frame)
lbl_width.grid(row=1, column=0)
entry_width = tk.Entry(frame, width=10)
entry_width.grid(row=1, column=1)

lbl_height = tk.Label(frame)
lbl_height.grid(row=2, column=0)
entry_height = tk.Entry(frame, width=10)
entry_height.grid(row=2, column=1)

keep_ratio_var = tk.BooleanVar()
chk_keep_ratio = tk.Checkbutton(frame, variable=keep_ratio_var)
chk_keep_ratio.grid(row=3, column=0, columnspan=2)

btn_resize = tk.Button(frame, command=resize_image)
btn_resize.grid(row=4, column=0, columnspan=2, pady=10)

# Initialisation de la langue
update_language()

root.mainloop()
