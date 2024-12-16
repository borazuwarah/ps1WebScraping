# pip install requests beautifulsoup4 openpyxl pandas
# pip install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup

# Paso 1: Descargar el contenido HTML y guardarlo en un archivo
url = "https://www.fhalmeria.com/pizarra-de-precios/almeria#CASI" 


# Realizar la solicitud GET para obtener el HTML de la página
response = requests.get(url)
response.raise_for_status()  # Si hay un error de conexión, generará una excepción

# Guardar el contenido en un archivo local
with open("htmlBruto.html", "w", encoding="utf-8") as file:
    file.write(response.text)

print("HTML descargado y guardado como htmlBruto.html")

# Paso 2: Procesar el archivo HTML para extraer las tablas
with open("htmlBruto.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, 'html.parser')

# Encuentra todas las tablas en el HTML
tablas = soup.find_all('table')

# Paso 3: Extraer datos de las tablas
for idx, tabla in enumerate(tablas, start=1):
    print(f"Extrayendo datos de la tabla {idx}...")
    
    # Encuentra todas las filas en la tabla
    filas = tabla.find_all('tr')
    
    # Para almacenar los datos extraídos
    datos_tabla = []
    
    for fila in filas:
        celdas = fila.find_all(['td', 'th'])  # 'td' para datos y 'th' para encabezados
        datos_fila = []
        
        for celda in celdas:
            # Limpiar contenido de etiquetas <span> y <i>, y solo mantener el texto relevante
            texto = celda.get_text(strip=True)
            
            # Si hay etiquetas como <span>, las procesamos de manera especial
            # Aquí tomamos solo el texto que está dentro de <strong>, por ejemplo
            if '<strong>' in str(celda):
                texto = ' '.join(celda.stripped_strings)
            
            datos_fila.append(texto)
        
        datos_tabla.append(datos_fila)
    
    # Mostrar la tabla extraída
    print(f"Datos de la tabla {idx}:")
    for fila in datos_tabla:
        print(fila)
    
    # Si necesitas guardar cada tabla en un archivo, puedes hacerlo con pandas o solo imprimirla
    # Aquí vamos a guardar cada tabla en un archivo de texto (opcional)
    with open(f"tabla_{idx}.txt", "w", encoding="utf-8") as f:
        for fila in datos_tabla:
            f.write("\t".join(fila) + "\n")
    
print("Extracción completada.")