# Instalacion del nuget
# Install-PackageProvider -Name NuGet -Force -Scope CurrentUser
# comprobacion del nuget
# Get-PackageProvider -Name NuGet


# Ruta del archivo Excel de salida
$outputFile = "DatosWeb.xlsx"

# URL de la página a analizar
$url = "https://www.fhalmeria.com/pizarra-de-precios/almeria#CASI" # Reemplaza con tu URL

# Realizamos la solicitud HTTP para obtener el contenido de la página
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Encontramos todas las filas de la tabla
table_rows = soup.select('table.pizarra_precios tbody tr')

# Creamos una lista para almacenar los datos extraídos
productos_precios = []

# Iteramos sobre cada fila
for row in table_rows:
    # Buscamos el nombre del producto en la primera columna (td)
    producto = row.find('td', style='min-width: 200px; text-align: center; font-size: 13px;')
    if producto:
        nombre_producto = producto.find('strong').text.strip()  # Extraemos el nombre del producto

        # Buscamos el precio (dentro de la etiqueta <strong> que tiene la clase "precio_caret-up" o "precio_caret-down")
        precio = row.find('td', {'data-title': '1º Precio'})
        if precio:
            # Extraemos el valor numérico del precio
            precio_value = precio.find('div')
            if precio_value:
                # Si el precio es una imagen (como en el ejemplo), lo procesamos
                precio_texto = precio_value.get('style', '')
                # Extraemos el número en el estilo de la URL de la imagen
                if 'url(/imagenes/numeros.png)' in precio_texto:
                    precio = precio_texto.split('url(/imagenes/numeros.png)')[-1].split('-')[0]
                    productos_precios.append([nombre_producto, precio])
                else:
                    productos_precios.append([nombre_producto, 'No disponible'])
            else:
                productos_precios.append([nombre_producto, 'No disponible'])
        else:
            productos_precios.append([nombre_producto, 'Precio no disponible'])

# Mostramos los datos obtenidos
for producto in productos_precios:
    print(producto)