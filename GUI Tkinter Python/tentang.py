import tkinter as tk
from tkinter import filedialog

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Tentang Aplikasi")
        master.configure(bg="white")  # Mengatur warna latar belakang GUI menjadi putih
        
        
        self.label = tk.Label(master, text="Tentang Aplikasi", font=("Helvetica", 14, "bold"),bg="white")
        self.label.pack( pady = 50,padx = 20,anchor="w")
        
        self.label = tk.Label(master, text="Aplikasi ini menggunakan metode K-Nearest Neighbor. Bahasa Pemrograman Python 3.11.2, Tkinter sebagai GUI untuk ", font=("Helvetica", 12),bg="white")
        self.label.pack(padx = 20,anchor="w" )
        
        self.label = tk.Label(master, text="Deteksi Kesegaran Ikan Kembung", font=("Helvetica", 12),bg="white")
        self.label.pack( padx = 20,anchor="w")
        
        self.label = tk.Label(master, text="", font=("Helvetica", 20),bg="white")
        self.label.pack(padx = 20, anchor="w")
        
        self.label = tk.Label(master, text="K-Nearest Neighbor (K-NN) adalah suatu metode yang menggunakan algoritma supervised dimana hasil dari query ", font=("Helvetica", 12),bg="white")
        self.label.pack(padx = 20,anchor="w")
        
        self.label = tk.Label(master, text="instance yang baru diklasifikasikan berdasarkan mayoritas dari label class pada K-NN. Dalam aplikasi ini, algoritma ini", font=("Helvetica", 12),bg="white")
        self.label.pack(padx = 20,anchor="w")
        
        self.label = tk.Label(master, text="dilatih untuk mengenali kesegaran ikan kembung", font=("Helvetica", 12),bg="white")
        self.label.pack(padx = 20,anchor="w")
        
        self.label = tk.Label(master, text="", font=("Helvetica", 20),bg="white")
        self.label.pack(padx = 20,anchor="w" )
        
        self.label = tk.Label(master, text="Untuk menggunakan aplikasi ini, pengguna dapat memilih menu deteksi kesegaran ikan kembung, algoritma akan ", font=("Helvetica", 12),bg="white")
        self.label.pack(padx = 20,anchor="w" )
        
        self.label = tk.Label(master, text="mendeteksi dan menampilkan kesegaran ikan kembung yang terdeteksi", font=("Helvetica", 12),bg="white")
        self.label.pack(padx = 20,anchor="w" )




# Inisialisasi Tkinter
root = tk.Tk()
my_gui = GUI(root)
root.geometry("1000x700")
root.mainloop()