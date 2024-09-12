import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageCropper(tk.Tk):
    def __init__(self):
        super().__init__()
        
        

        self.title("Preprocessing Image Cropper")
        self.geometry("1000x700")
        
        self.image = None
        self.tk_image = None
        self.rect = None
        self.start_x = None
        self.start_y = None
        
        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.canvas_frame, cursor="cross")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.vbar = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.vbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.hbar = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.hbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        
        bold_font = ('Helvetica', 10, 'bold')
        self.open_button = tk.Button(self, text="Buka Citra", command=self.open_image, width=30, height=1, bg="#00FFFF", fg="black", font=bold_font)
        self.open_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.crop_button = tk.Button(self, text="Crop Citra", command=self.crop_image, width=30, height=1, bg="#00FFFF", fg="black", font=bold_font)
        self.crop_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.save_button = tk.Button(self, text="Simpan Citra", command=self.save_image, width=30, height=1, bg="#00FFFF", fg="black", font=bold_font)
        self.save_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.canvas.create_text(800, 20, text="Image Cropper", fill="Black", font=('Helvetica', 20, 'bold'))

        
    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)

            self.image = self.image.resize((640, 640), Image.Resampling.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(self.image)

            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
            self.canvas.create_text(800, 20, text="Image Cropper", fill="Black", font=('Helvetica', 20, 'bold'))
    
    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')
        
    
    def on_mouse_drag(self, event):
        curX, curY = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)
    
    def on_button_release(self, event):
        pass
    
    def crop_image(self):
        if self.image and self.rect:
            x1, y1, x2, y2 = self.canvas.coords(self.rect)
            cropped_image = self.image.crop((x1, y1, x2, y2))
            self.tk_image = ImageTk.PhotoImage(cropped_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
            self.image = cropped_image
            self.canvas.create_text(800, 20, text="Image Cropper", fill="Black", font=('Helvetica', 20, 'bold'))
    
    def save_image(self):
        if self.image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if file_path:
                self.image.save(file_path)

if __name__ == "__main__":
    app = ImageCropper()
    app.mainloop()
