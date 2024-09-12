import os
import cv2
import numpy as np
import pandas as pd
from skimage.feature import graycomatrix, graycoprops
import matplotlib.pyplot as plt
from sklearn import metrics

file = '../PROGRAM/basisdatafitur.xlsx'
dataset = pd.read_excel(file)
glcm_properties = ['dissimilarity', 'correlation', 'homogeneity', 'contrast', 'energy']
jenis = ['ikansegar','ikanbusuk']
aktual = []

# Mengisi array kelas dengan nilai "ikansegar" dan "ikanbusuk" secara bergantian
for i in jenis:
    aktual.extend([i] * 50)

# Konversi array kelas ke dalam numpy array
aktual = np.array(aktual)


fitur = dataset.iloc[:, 1:-1].values
kelas = dataset.iloc[:, 24].values
tes_fitur = []

# Tentukan path folder secara manual
folder_path = 'uji/'

# Loop melalui semua file di folder
for filename in os.listdir(folder_path):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image_path = os.path.join(folder_path, filename)
        print(image_path)

        # Preprocessing
        src = cv2.imread(image_path, 1)
        src = cv2.resize(src, (640, 640))

        tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        _, alpha = cv2.threshold(tmp, 140, 255, cv2.THRESH_BINARY_INV)
        alpha = cv2.dilate(alpha.copy(), None, iterations=20)
        alpha = cv2.erode(alpha.copy(), None, iterations=25)
        b, g, r = cv2.split(src)
        rgba = [b, g, r, alpha]
        dst = cv2.merge(rgba, 4)

        contours, hierarchy = cv2.findContours(alpha, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        selected = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(selected)
        cropped = dst[y:y + h, x:x + w]
        gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

        # RGB-HSV
        hsv_image = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
        H = np.mean(hsv_image[:, :, 0])
        S = np.mean(hsv_image[:, :, 1])
        V = np.mean(hsv_image[:, :, 2])

        fitur_gambar = [H, S, V]

        # GLCM
        glcm = graycomatrix(gray, distances=[5], angles=[0, np.pi / 4, np.pi / 2, 3 * np.pi / 4], levels=256, symmetric=True, normed=True)
        glcm_props = [prop for name in glcm_properties for prop in graycoprops(glcm, name)[0]]
        fitur_gambar.extend(glcm_props)

        tes_fitur.append(fitur_gambar)

# Konversi tes_fitur ke numpy array
tes_fitur = np.array(tes_fitur)




# Klasifikasi menggunakan algoritma K-Nearest Neighbors
predictions = []
for test_point in tes_fitur:
    distances = []
    for train_point in fitur:
        distance = np.linalg.norm(test_point - train_point)
        distances.append(distance)
    sorted_indices = np.argsort(distances)
    k_nearest_indices = sorted_indices[:3]  # K=3
    k_nearest_labels = kelas[k_nearest_indices]
    unique_labels, label_counts = np.unique(k_nearest_labels, return_counts=True)
    predicted_label = unique_labels[np.argmax(label_counts)]
    predictions.append(predicted_label)

kelas_pred = np.array(predictions)

# Hitung akurasi secara manual
correct_predictions = sum(aktual == kelas_pred)
total_predictions = len(aktual)
accuracy = correct_predictions / total_predictions * 100
print(f"Akurasi: {accuracy}%")

# Print prediksi kelas
print(kelas_pred)

# Buat laporan klasifikasi manual
def classification_report_manual(aktual, kelas_pred, labels):
    report = {}
    for label in labels:
        tp = sum((aktual == label) & (kelas_pred == label))
        fp = sum((aktual != label) & (kelas_pred == label))
        fn = sum((aktual == label) & (kelas_pred != label))
        tn = sum((aktual != label) & (kelas_pred != label))
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        report[label] = {
            'precision': precision,
            'recall': recall,
            'f1-score': f1_score,
            'support': sum(aktual == label)
        }
    
    return report

labels = np.unique(aktual)
report = classification_report_manual(aktual, kelas_pred, labels)
for label, metrics in report.items():
    print(f"Class {label}:")
    print(f"  Precision: {metrics['precision']:.2f}")
    print(f"  Recall: {metrics['recall']:.2f}")
    print(f"  F1-score: {metrics['f1-score']:.2f}")
    print(f"  Support: {metrics['support']}")

# Hitung confusion matrix 
def confusion_matrix_manual(aktual, kelas_pred, labels):
    matrix = np.zeros((len(labels), len(labels)), dtype=int)
    label_to_index = {label: index for index, label in enumerate(labels)}
    for a, p in zip(aktual, kelas_pred):
        matrix[label_to_index[a], label_to_index[p]] += 1
    return matrix

conf_matrix = confusion_matrix_manual(aktual, kelas_pred, labels)

# Plot confusion matrix 
plt.figure(figsize=(10, 7))
plt.imshow(conf_matrix, interpolation='nearest', cmap='Blues')
plt.title('Confusion Matrix')
plt.colorbar()

tick_marks = np.arange(len(labels))
plt.xticks(tick_marks, labels, rotation=45)
plt.yticks(tick_marks, labels)

thresh = conf_matrix.max() / 2
for i, j in np.ndindex(conf_matrix.shape):
    plt.text(j, i, format(conf_matrix[i, j], 'd'),
             ha="center", va="center",
             color="white" if conf_matrix[i, j] > thresh else "black")

plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()