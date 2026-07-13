import tkinter as tk
from tkinter import filedialog, messagebox
from ai.proccesor import run_pipeline

def select_image_and_run():
    image_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.jpeg *.png")]
    )
    if not image_path:
        return 

    chosen_font = font_var.get()  ''

    try:
        run_pipeline(image_path, chosen_font)
        messagebox.showinfo("Success", "PDF generated successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("AI Document Scanner")
root.geometry("400x200")

tk.Label(root, text="Choose a font:").pack(pady=5)
font_var = tk.StringVar(value="Arial")
font_dropdown = tk.OptionMenu(root, font_var, "Arial", "Times New Roman", "Courier New")
font_dropdown.pack(pady=5)

tk.Button(root, text="Select Image & Generate PDF", command=select_image_and_run).pack(pady=20)

root.mainloop()