import tkinter as tk
import cv2
import xlsxwriter 
from skimage.feature import graycomatrix, graycoprops
from tkinter import messagebox
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Melatih Dataset")
        master.configure(bg="white")  # Mengatur warna latar belakang GUI menjadi putih
        
        
         # Font tebal
        bold_font = ('Helvetica', 10, 'bold')
        
        self.label = tk.Label(master, text="Klasifikasi KNN", font=("Helvetica", 15, "bold"),bg="white")
        self.label.pack(pady=5)
        
        self.k_label = tk.Label(master, text="Nilai k:")
        self.k_label.pack(pady=5,)

        self.k_entry = tk.Entry(master, justify="center", font=("Helvetica", 12, "bold"))
        self.k_entry.pack(pady=5)
        
        # Buat label untuk menampilkan akurasi
        self.label_akurasi = tk.Label(master, text="Akurasi : none", font=('Helvetica', 12, "bold"),bg="white")
        self.label_akurasi.pack( padx=20, pady=40, )
        
        self.buttonekstraksi = tk.Button(master, text="Pelatihan Dataset", command=self.Ekstraksi, width=30, height=1, bg="#00FFFF", fg="black", font=bold_font)
        self.buttonekstraksi.pack(side=tk.LEFT, padx=100, pady=40, anchor=tk.NE)
        
        self.buttontraining = tk.Button(master, text="Cari Akurasi", command=self.training, width=30, height=1, bg="#00FFFF", fg="black", font=bold_font)
        self.buttontraining.pack(side=tk.LEFT, padx=130, pady=40, anchor=tk.NE)

        
    def Ekstraksi(self):
          try:
            workbook = xlsxwriter.Workbook('../PROGRAM/basisdatafitur2.xlsx')
            worksheet = workbook.add_worksheet()

            jenis = ['ikanbusuk','ikansegar']
            jum_per_data = 300

            hsv_properties = ['hue','saturation','value']
            glcm_properties = ['dissimilarity', 'correlation', 'homogeneity', 'contrast', 'energy']
            angles = ['0', '45', '90','135']

            worksheet.write(0,0,'File')
            kolom = 1

            # Writing excel header
            for i in hsv_properties:
                worksheet.write(0,kolom,i)
                kolom+=1
            for i in glcm_properties:
                for j in angles:
                    worksheet.write(0,kolom,i+" "+j)
                    kolom+=1

            worksheet.write(0,kolom,'Class')
            kolom+=1
            baris = 1

            for i in jenis:
                for j in range(1,26):        
                    kolom     = 0
                    file_name = "../PROGRAM/dataset/" + i + str(j) + ".jpg"
                    print(file_name)
                    worksheet.write(baris,kolom,file_name)
                    kolom+=1
                    src     = cv2.imread(file_name, 1)
                    #preprocesssng
                    src     = cv2.resize(src, (640, 640))
                    
                    #segmentasi
                    tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
                    _, mask = cv2.threshold(tmp, 140, 255, cv2.THRESH_BINARY_INV)
                    mask = cv2.dilate(mask.copy(), None, iterations=20)
                    mask = cv2.erode(mask.copy(), None, iterations=25)
                    b, g, r = cv2.split(src)
                    rgba = [b, g, r, mask]
                    dst = cv2.merge(rgba, 4)

                    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    selected = max(contours, key=cv2.contourArea)
                    x, y, w, h = cv2.boundingRect(selected)
                    cropped = dst[y:y + h, x:x + w]
                    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
                    

                    # RGB-HSV
                    hsv_image   = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
                    H = hsv_image[:,:,0]
                    S = hsv_image[:,:,1]
                    V = hsv_image[:,:,2]
                    
                    H = np.mean(H)
                    S = np.mean(S)
                    V = np.mean(V)
                    
                    worksheet.write(baris,kolom,H)
                    kolom+=1
                    worksheet.write(baris,kolom,S)
                    kolom+=1
                    worksheet.write(baris,kolom,V)
                    kolom+=1

                    #GLCM
                    glcm = graycomatrix(gray, distances=[5], angles=[0, np.pi/4, np.pi/2, 3*np.pi/4],
                               levels=256, symmetric=True, normed=True)
                                            
                    glcm_props = [property for name in glcm_properties for property in graycoprops(glcm, name)[0]]
                    for item in glcm_props:            
                        worksheet.write(baris,kolom,item)
                        kolom+=1

                    worksheet.write(baris,kolom,i)
                    kolom+=1
                    baris+=1
            workbook.close()
          except Exception as e:
            print("An error occurred:", e)
# --------------------------
    def training(self):
        try:
         #--------------- klasifikasi knn
            df = pd.read_excel('../PROGRAM/basisdatafitur.xlsx')
            X = df.iloc[:,+1:-1].values
            y = df['Class'].values 
            
            X_train, X_test, y_train, y_test = train_test_split( X, y,test_size=0.30, random_state=12, stratify=y)

   

            
            k = int(self.k_entry.get())
  
             # Implementasi KNN 
            y_pred = []

            for test_point in X_test:
                # Menghitung jarak Euclidean dari test_point ke semua titik di X_train
                distances = np.sqrt(np.sum((X_train - test_point) ** 2, axis=1))
                
                # Mendapatkan indeks dari k jarak terkecil
                k_indices = np.argsort(distances)[:k]
                
                # Mendapatkan label dari k tetangga terdekat
                k_nearest_labels = [y_train[i] for i in k_indices]
                
                # Tentukan prediksi dengan mayoritas
                unique_labels, counts = np.unique(k_nearest_labels, return_counts=True)
                majority_label = unique_labels[np.argmax(counts)]
                y_pred.append(majority_label)

            y_pred = np.array(y_pred)

            # Hitung akurasi
            correct_predictions = sum(y_test == y_pred)
            total_predictions = len(y_test)
            accuracy = correct_predictions / total_predictions

            # Tampilkan akurasi
            print(f"Akurasi: {accuracy*100}%")
            self.label_akurasi.config(text=f"Akurasi: {accuracy*100}%")
     
        except Exception as e:
            print("An error occurred:", e)
            messagebox.showinfo("Kesalahan", "masukkan Nilai K terlebih dahulu !")

# Inisialisasi Tkinter
root = tk.Tk()
my_gui = GUI(root)
root.geometry("1000x700")
root.mainloop()