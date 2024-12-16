from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configuración de las opciones del navegador para habilitar los logs de rendimiento
options = Options()
options.add_argument('--headless')  # Ejecutar sin abrir el navegador
options.add_argument('--no-sandbox')  # Opciones adicionales para evitar posibles bloqueos
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--enable-logging')  # Habilitar los logs
options.add_argument('--v=1')  # Nivel de detalle de los logs
options.add_argument('--remote-debugging-port=9222')  # Habilitar puerto de depuración remota

# Iniciar el navegador con las opciones configuradas
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)








# URL de la página que deseas scrapear
url = "https://www.fhalmeria.com/pizarra-de-precios/almeria#CASI" 

driver.get(url)

# Esperar un poco para que cargue la página y las solicitudes de red
time.sleep(10)

# Obtener los logs de rendimiento
logs = driver.get_log('performance')  # Intentar con 'performance' # Cambiar a 'browser' para obtener logs de red

# Filtrar las solicitudes de red que contienen respuestas
for log in logs:
    message = log['message']
    if 'Network.response' in message:  # Ver si contiene una respuesta de red
        print(message)

# Cerrar el navegador
driver.quit()