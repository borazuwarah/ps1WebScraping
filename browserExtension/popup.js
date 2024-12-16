document.getElementById('extraerDatos').addEventListener('click', function() {
    console.log("Botón Extraer Datos presionado");

    // Obtener la pestaña activa
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        const tab = tabs[0];
        if (tab) {
            console.log("Intentando ejecutar el script en la pestaña activa...");
            chrome.scripting.executeScript({
                target: { tabId: tabs[0].id },
                func: extractTableData
            }).then(() => {
                console.log("Script ejecutado correctamente");
            }).catch((error) => {
                console.error("Error al ejecutar el script:", error);
            });
        } else {
            console.error("No se pudo obtener la pestaña activa");
        }
    });
});

// Función de extracción de datos de la tabla
function extractTableData() {
    console.log("Ejecutando extracción de datos de la tabla...");
    const tablas = document.querySelectorAll('.pizarra_precios');
    console.log("Tablas encontradas:", tablas.length);

    if (tablas.length > 0) {
        tablas.forEach((tabla, index) => {
            console.log(`Extrayendo datos de la tabla ${index + 1}:`);
            const filas = tabla.querySelectorAll('tr');
            filas.forEach((fila, filaIndex) => {
                const celdas = fila.querySelectorAll('td');
                const datos = [];
                celdas.forEach((celda, celdaIndex) => {
                    datos.push(celda.innerText.trim());
                });
                console.log(`Fila ${filaIndex + 1}:`, datos);
            });
        });
    } else {
        console.log("No se encontraron tablas con la clase 'pizarra_precios'.");
    }
}
