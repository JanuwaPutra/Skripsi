import tkinter as tk
import cv2
import numpy as np
import pandas as pd
from tkinter import messagebox, filedialog
from skimage.feature import graycomatrix, graycoprops
from PIL import Image, ImageTk
import os

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Deteksi Kesegaran Ikan kembung")
        master.configure(bg="white")  # Mengatur warna latar belakang GUI menjadi putih
        
         # Font tebal
        bold_font = ('Helvetica', 10, 'bold')
        
        self.label = tk.Label(master, text="Deteksi Kesegaran Ikan Kembung", font=("Helvetica", 15, "bold"),bg="white")
        self.label.pack(pady=5)
        
        self.k_label = tk.Label(master, text="Nilai k:")
        self.k_label.pack(pady=5,)

        self.k_entry = tk.Entry(master, justify="center", font=("Helvetica", 12, "bold"))
        self.k_entry.pack(pady=5)
        
        # Buat label untuk menampilkan akurasi
        self.label_deteksi = tk.Label(master, text="Hasil Deteksi : none", font=('Helvetica', 12, "bold"),bg="white")
        self.label_deteksi.pack( padx=20, pady=40, )
        
        self.buttonbrowse = tk.Button(master, text="Buka Citra", command=self.browse, width=30, height=1, bg="#00FFFF", fg="black", font=bold_font)
        self.buttonbrowse.pack(side=tk.LEFT, padx=40, pady=40, anchor=tk.NE)

        self.buttonDeteksi = tk.Button(master, text="Deteksi", command=self.Deteksi, width=30, height=1, bg="#00FFFF", fg="black", font=bold_font)
        self.buttonDeteksi.pack(side=tk.LEFT, padx=40, pady=40, anchor=tk.NE)
        
        self.buttoneuclidean = tk.Button(master, text="Cari Jarak euclidean", command=self.jarak, width=30, height=1, bg="#00FFFF", fg="black", font=bold_font)
        self.buttoneuclidean.pack( pady=40)
        
        # Inisialisasi label untuk menampilkan gambar
        self.image_label = tk.Label(master)
        self.image_label.pack(padx=20, pady=20, anchor="w")
        
        
        
        
     # Metode baru untuk menampilkan gambar yang dipilih
    def display_image(self, file_path):
        image = Image.open(file_path)
        image = image.resize((300, 300))  # Sesuaikan ukuran gambar sesuai kebutuhan
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo  # Simpan referensi agar gambar tetap ditampilkan
        
 
    def browse(self):
        self.file_path = filedialog.askopenfilename(initialdir="../PROGRAM/uji/", title="Select Image File",
                                                    filetypes=(("Image files", "*.jpg;*.png;*.jpeg"), ("all files", "*.*")))
        print("File selected:", self.file_path)
        self.display_image(self.file_path)
        
        
    # --------------------------
    def jarak(self):
      try:
            file        = '../PROGRAM/basisdatafitur.xlsx'
            dataset     = pd.read_excel(file)
            glcm_properties = ['dissimilarity', 'correlation', 'homogeneity', 'contrast', 'energy']

            fitur       = dataset.iloc[:,+1:-1].values
            tes_fitur   = []
            tes_fitur.append([])
            

            # Preprocessing
            src     = cv2.imread(self.file_path, 1)
            src     = cv2.resize(src, (640, 640))

            #segmentasi
            tmp     = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
            _,mask  = cv2.threshold(tmp,140,255,cv2.THRESH_BINARY_INV)
            mask    = cv2.dilate(mask.copy(),None,iterations=20)
            mask    = cv2.erode(mask.copy(),None,iterations=25)
            b, g, r = cv2.split(src)
            rgba    = [b,g,r, mask]
            dst     = cv2.merge(rgba,4)

            contours,hierarchy    = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            selected    = max(contours,key=cv2.contourArea)
            x,y,w,h     = cv2.boundingRect(selected)
            cropped     = dst[y:y+h,x:x+w]
            gray        = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    
            # RGB-HSV
            hsv_image   = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
           
            H = hsv_image[:,:,0]
            S = hsv_image[:,:,1]
            V = hsv_image[:,:,2]
                    
            H = np.mean(H)
            S = np.mean(S)
            V = np.mean(V)

            tes_fitur[0].append(H)
            tes_fitur[0].append(S)
            tes_fitur[0].append(V)

            # GLCM

            # Calculate GLCM with desired distances
            glcm = graycomatrix(gray, distances=[5], angles=[0, np.pi/4, np.pi/2, 3*np.pi/4],
                   levels=256, symmetric=True, normed=True)
            feature = []
            glcm_props = [propery for name in glcm_properties for propery in graycoprops(glcm, name)[0]]
            for item in glcm_props:            
             tes_fitur[0].append(item)


            # --------------------------------------------------
            # Menghitung mean dan standar deviasi dari data fitur
            mean = np.mean(fitur, axis=0)
            std_dev = np.std(fitur, axis=0)

            # Menstandarisasi data fitur dan data uji menggunakan mean dan standar deviasi
            fitur = (fitur - mean) / std_dev
            tes_fitur = (tes_fitur - mean) / std_dev
            
            #print(tes_fitur)
            
            # Menghitung jarak Euclidean secara manual
            data_jarak = np.sqrt(np.sum(np.square(fitur - tes_fitur), axis=1))

            # Kolom yang ingin Anda tampilkan
            columns_to_display = ['File', 'Class']

            # Membaca file Excel dan memilih hanya kolom-kolom tertentu
            selected_columns_data = pd.read_excel(file, usecols=columns_to_display)
            selected_columns_data['jarak euclidean'] = data_jarak
            selected_columns_data = selected_columns_data.sort_values(by=['jarak euclidean'], ascending=True)
            # Menyimpan data yang telah diurutkan ke dalam file Excel baru
            selected_columns_data.to_excel('../PROGRAM/jarakeuclidean.xlsx', index=False)
            
            def buka_file_excel(nama_file):
                # Untuk platform lain seperti Linux atau MacOS
                os.startfile(nama_file)

            # Ganti 'nama_file.xlsx' dengan nama file Excel yang ingin Anda buka
            buka_file_excel('jarakeuclidean.xlsx')
           

      except Exception as e:
            print("An error occurred:", e)
            messagebox.showinfo("Kesalahan", "masukkan Citra terlebih dahulu !")
# --------------------------
    def Deteksi(self):
     try:
            file        = '../PROGRAM/basisdatafitur.xlsx'
            dataset     = pd.read_excel(file)
            glcm_properties = ['dissimilarity', 'correlation', 'homogeneity', 'contrast',  'energy']

            fitur       = dataset.iloc[:,+1:-1].values
            kelas       = dataset.iloc[:,24].values
            tes_fitur   = []
            tes_fitur.append([])
         
            # Feature extraction for data testing----------------------------------------------
            # Preprocessing
            src = cv2.imread(self.file_path, 1)
            src     = cv2.resize(src, (640, 640))

            #segmentasi
            tmp     = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
            _,mask  = cv2.threshold(tmp,140,255,cv2.THRESH_BINARY_INV)
            mask    = cv2.dilate(mask.copy(),None,iterations=20)
            mask    = cv2.erode(mask.copy(),None,iterations=25)
            b, g, r = cv2.split(src)
            rgba    = [b,g,r, mask]
            dst     = cv2.merge(rgba,4)

            contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            selected    = max(contours,key=cv2.contourArea)
            x,y,w,h     = cv2.boundingRect(selected)
            cropped     = dst[y:y+h,x:x+w]
            mask        = mask[y:y+h,x:x+w]
            gray        = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
            
            # RGB-HSV
            hsv_image   = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
           
            H = hsv_image[:,:,0]
            S = hsv_image[:,:,1]
            V = hsv_image[:,:,2]
                    
            H = np.mean(H)
            S = np.mean(S)
            V = np.mean(V)

            tes_fitur[0].append(H)
            tes_fitur[0].append(S)
            tes_fitur[0].append(V)

            # GLCM

            # Calculate GLCM with desired distances
            glcm = graycomatrix(gray, distances=[5], angles=[0, np.pi/4, np.pi/2, 3*np.pi/4],
                   levels=256, symmetric=True, normed=True)
            glcm_props = [propery for name in glcm_properties for propery in graycoprops(glcm, name)[0]]
            for item in glcm_props:            
             tes_fitur[0].append(item)


            # --------------------------------------------------
            # Menghitung mean dan standar deviasi dari data fitur
            mean = np.mean(fitur, axis=0)
            std_dev = np.std(fitur, axis=0)

            # Menstandarisasi data fitur dan data uji menggunakan mean dan standar deviasi
            fitur = (fitur - mean) / std_dev
            tes_fitur = (tes_fitur - mean) / std_dev

            # Hitung jarak euclidean secara manual
            distances = np.sqrt(np.sum(np.square(fitur - tes_fitur), axis=1))

            # Sortir indeks berdasarkan jarak dan ambil k terdekat
            k = int(self.k_entry.get())
            nearest_indices = np.argsort(distances)[:k]

            # Ambil kelas dari indeks terdekat
            nearest_classes = kelas[nearest_indices]

            # Hitung kelas yang paling sering muncul
            unique_classes, counts = np.unique(nearest_classes, return_counts=True)
            y_pred = unique_classes[np.argmax(counts)]

            if 'segar' in y_pred:
                hasil = 'Ikan Kembung Segar'
            else:
                hasil = 'Ikan Kembung Busuk'

            print(y_pred)


            self.label_deteksi.config(text=f"Hasil Deteksi: {hasil}")
           

     except Exception as e:
            print("An error occurred:", e)
            messagebox.showinfo("Kesalahan", "masukkan Citra atau Nilai K terlebih dahulu !")
            
            
    

# Inisialisasi Tkinter
root = tk.Tk()
my_gui = GUI(root)
root.geometry("1000x700")
root.mainloop()