# install
# pip install selenium pillow pytesseract pandas openpyxl
# https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.3.0.20221214.exe




import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image, ImageEnhance
import pytesseract
import pandas as pd
import requests

# Configurar ruta de Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Configurar Selenium (ajusta la ruta del driver según tu instalación)
chrome_service = Service(r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe')  # Cambia a la ubicación de tu chromedriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Ejecutar sin ventana visible (opcional)
driver = webdriver.Chrome(service=chrome_service, options=options)

# URL de la página
url = "https://www.fhalmeria.com/pizarra-de-precios/almeria#CASI"

# Función para descargar imágenes
def download_image(url, path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(path, 'wb') as f:
            f.write(response.content)

# Función para procesar una imagen con OCR
def process_image_with_ocr(image_path):
    image = Image.open(image_path)
    image = image.convert('L')  # Escala de grises
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)  # Aumentar contraste
    text = pytesseract.image_to_string(image, config='--psm 6 digits')
    return text.strip()

# Abrir la página y esperar a que se cargue la tabla
driver.get(url)
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tabla_precios")))

# Encontrar todas las tablas dinámicas
tables = driver.find_elements(By.CLASS_NAME, "tabla_precios")

# Crear carpeta para imágenes
os.makedirs('imagenes', exist_ok=True)

data = []  # Almacenará las filas extraídas

# Recorrer cada tabla
for table_index, table in enumerate(tables):
    rows = table.find_elements(By.TAG_NAME, "tr")  # Filas de la tabla
    for row_index, row in enumerate(rows):
        cells = row.find_elements(By.TAG_NAME, "td")  # Celdas de cada fila
        row_data = []
        for cell_index, cell in enumerate(cells):
            # Verificar si contiene una imagen
            img_tag = cell.find_elements(By.TAG_NAME, "img")
            if img_tag:
                img_url = img_tag[0].get_attribute("src")
                img_path = f"imagenes/table_{table_index}_row_{row_index}_cell_{cell_index}.png"
                download_image(img_url, img_path)  # Descargar imagen
                text = process_image_with_ocr(img_path)  # Extraer texto con OCR
                row_data.append(text)
            else:
                row_data.append(cell.text)  # Agregar texto normal
        if row_data:  # Si la fila contiene datos, agregarla
            data.append(row_data)

driver.quit()  # Cerrar el navegador

# Crear un DataFrame y exportar a Excel
df = pd.DataFrame(data)
df.to_excel("resultado_tablas.xlsx", index=False, header=False)

print("¡Extracción completada! Los datos se han guardado en 'resultado_tablas.xlsx'.")