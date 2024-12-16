console.log("content.js cargado correctamente");

// Comenzamos con la depuración al cargar el DOM
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM completamente cargado.");

    // Buscamos las tablas con la clase 'pizarra_precios'
    setTimeout(() => {
        console.log("Buscando tablas...");
        const tablas = document.querySelectorAll('.pizarra_precios');
        console.log("Número de tablas encontradas: " + tablas.length);

        if (tablas.length > 0) {
            tablas.forEach((tabla, index) => {
                console.log(`Extrayendo datos de la tabla ${index + 1}:`);
                const filas = tabla.querySelectorAll('tr');
                console.log(`Número de filas en la tabla ${index + 1}: ${filas.length}`);

                filas.forEach((fila, filaIndex) => {
                    const celdas = fila.querySelectorAll('td');
                    const datos = [];
                    celdas.forEach((celda, celdaIndex) => {
                        // Mostramos cada celda por separado para depurar
                        console.log(`Celda ${celdaIndex + 1} en fila ${filaIndex + 1}:`, celda.innerText.trim());
                        datos.push(celda.innerText.trim());
                    });

                    if (datos.length > 0) {
                        console.log(`Datos extraídos de la fila ${filaIndex + 1}:`, datos);  // Mostramos los datos extraídos de la fila
                    }
                });
            });
        } else {
            console.log("No se encontraron tablas con la clase 'pizarra_precios'.");
        }
    }, 2000);  // Esperamos 2 segundos para asegurarnos de que las tablas se hayan cargado
});
