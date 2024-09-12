import tkinter as tk
from PIL import Image, ImageTk
import subprocess


class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Deteksi Kesegaran Ikan Kembung")
        master.configure(bg="white")  # Mengatur warna latar belakang GUI menjadi putih
        
        # Buat label untuk menampilkan gambar
        self.image_label = tk.Label(master)
        self.image_label.pack(side=tk.LEFT, anchor=tk.NW)  # Mengatur anchor ke NW dan padding

        # Buka gambar menggunakan PIL
        image = Image.open("background.jpg")
        # Resize gambar agar sesuai dengan label
        image = image.resize((500, 700))
        # Konversi gambar ke format yang dapat ditampilkan oleh Tkinter
        photo = ImageTk.PhotoImage(image)

        self.image_label.configure(image=photo)
        self.image_label.image = photo

        
         # Font tebal
        bold_font = ('Helvetica', 10, 'bold')
        
        self.label = tk.Label(master, text="Deteksi Kesegaran Ikan Kembung", font=("Helvetica", 20, "bold"),bg="white")
        self.label.pack(pady=50)
        
        self.buttontentang = tk.Button(master, text="Tentang Aplikasi", command=self.tentang, width=30, height=1, bg="#00FFFF", fg="black", font=bold_font)
        self.buttontentang.pack( padx=130, pady=10, anchor=tk.NE)
        
        self.buttonpreprocessing = tk.Button(master, text="Preprocessing", command=self.preprocessing, width=30, height=1, bg="#00FFFF", fg="black", font=bold_font)
        self.buttonpreprocessing.pack( padx=130, pady=10, anchor=tk.NE)
        
        
        self.buttontraining = tk.Button(master, text="Melatih Dataset", command=self.training, width=30, height=1, bg="#00FFFF", fg="black", font=bold_font)
        self.buttontraining.pack( padx=130, pady=10, anchor=tk.NE)
        
        self.buttonidentifikasi = tk.Button(master, text="Deteksi Kesegaran ikan Kembung", command=self.identifikasi, width=30, height=1, bg="#00FFFF", fg="black", font=bold_font)
        self.buttonidentifikasi.pack( padx=130, pady=10, anchor=tk.NE)
        

    def tentang(self):
        filename = ("GUI Tkinter Python/tentang.py")
        if filename:
         subprocess.Popen(['python', filename])
         
    def training(self):
        filename = ("GUI Tkinter Python/training.py")
        if filename:
         subprocess.Popen(['python', filename])
    def identifikasi(self):
        filename = ("GUI Tkinter Python/deteksi.py")
        if filename:
         subprocess.Popen(['python', filename])
    def preprocessing(self):
        filename = ("GUI Tkinter Python/preprocessing.py")
        if filename:
         subprocess.Popen(['python', filename])
   

# Inisialisasi Tkinter
root = tk.Tk()
my_gui = GUI(root)
root.geometry("1000x700")
root.mainloop()
