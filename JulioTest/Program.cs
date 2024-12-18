using HtmlAgilityPack;
using System.Text.RegularExpressions;

class Program
{
    static async Task Main(string[] args)
    {
        string url = "https://www.fhalmeria.com/pizarra-de-precios/almeria#CASI";

        try
        {
            Console.WriteLine($"url: {url}");
            // Descargar HTML desde la URL
            var html = await DescargarHtml(url);

            // Cargar el HTML en HtmlAgilityPack
            var doc = new HtmlDocument();
            doc.LoadHtml(html);

            // Seleccionar todas las tablas y títulos
            var titulos = doc.DocumentNode.SelectNodes("//h3[@style]");
            var tablas = doc.DocumentNode.SelectNodes("//table");

            if (tablas == null)
            {
                Console.WriteLine("No tables in this page.");
                return;
            }

            if (titulos == null || titulos.Count <= tablas.Count)
            {
                Console.WriteLine("There are more tables than titles.");
                return;
            }

            // Ignorar el primer título
            var titulosRelevantes = titulos.Skip(1).ToList();

            if (titulosRelevantes.Count != tablas.Count)
            {
                Console.WriteLine("Total of titles doesn't match with total of tables.");
                return;
            }

            for (int i = 0; i < tablas.Count; i++)
            {
                var tabla = tablas[i];
                var titulo = titulosRelevantes[i].InnerText.Trim();


                string fileName = $"Extracted_{DateTime.Now:yyyyMMdd_HHmmss}_{ClearTitle(titulo)}";
                Console.WriteLine($"Processing table, title: {titulo}");

                var filas = tabla.SelectNodes(".//tr");
                if (filas == null) continue;

                List<string[]> datosTabla = new List<string[]>();

                foreach (var fila in filas)
                {
                    var celdas = fila.SelectNodes(".//td|.//th"); 
                    if (celdas == null) continue;

                    List<string> filaDatos = new List<string>();

                    bool primeraColumnaTexto = true; 
                    bool segundaColumnaOmitida = false; 
                    foreach (var celda in celdas)
                    {
                        var div = celda.SelectSingleNode(".//div[@style]");
                        if (div != null)
                        {
                            var style = div.GetAttributeValue("style", "");

                            if (!string.IsNullOrEmpty(style) && style.Contains("background"))
                            {
                                if (primeraColumnaTexto)
                                    primeraColumnaTexto = false;
                                
                                else if (!segundaColumnaOmitida)
                                {
                                    segundaColumnaOmitida = true;
                                    continue;
                                }
                                else
                                {
                                    var coordenadas = ExtractCoordenates(style);
                                    if (coordenadas.HasValue)
                                    {
                                        var valor = CalcularNumeroDeSalida(coordenadas.Value.Item2, coordenadas.Value.Item1);
                                        filaDatos.Add(valor.ToString());
                                    }
                                    else
                                        filaDatos.Add("null");

                                }
                            }
                        }
                        else
                        {
                            // Extraer texto normal de la celda
                            var texto = celda.InnerText.Trim();

                            if (primeraColumnaTexto)
                            {
                                // Agregar solo la primera columna de texto
                                filaDatos.Add(texto == "&nbsp;" ? "null" : texto);
                                primeraColumnaTexto = false;
                            }
                            else if (!segundaColumnaOmitida)
                            {
                                // Omitir la segunda columna numérica
                                segundaColumnaOmitida = true;
                                continue; 
                            }
                            else
                                filaDatos.Add(texto == "&nbsp;" ? "null" : texto);
                            
                        }
                    }
                    datosTabla.Add(filaDatos.ToArray());
                }

                // Exportar datos de la tabla a CSV
                ExportarCsv(datosTabla, fileName);
                Console.WriteLine($"Table exported, title: {fileName}");
            }

            Console.WriteLine("completd process.");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error: {ex.Message}");
        }
    }


    /// <summary>
    /// clean tittle
    /// </summary>
    /// <param name="title"></param>
    /// <returns></returns>
    static string ClearTitle(string title)
    {
        // Reemplazar caracteres no válidos para nombres de archivo
        var nombre = title
            .Replace(" ", "_")
            .Replace("<strong>", "")
            .Replace("</strong>", "")
            .Replace(":", "")
            .Replace("/", "-")
            .Replace("\\", "-")
            .Replace("*", "")
            .Replace("?", "")
            .Replace("\"", "")
            .Replace("<", "")
            .Replace(">", "")
            .Replace("|", "");
        return $"{nombre}.csv";
    }


    /// <summary>
    /// download HTML content
    /// </summary>
    /// <param name="url"></param>
    /// <returns></returns>
    static async Task<string> DescargarHtml(string url)
    {
        using (var client = new HttpClient())
        {
            var response = await client.GetAsync(url);
            response.EnsureSuccessStatusCode();

            var html = await response.Content.ReadAsStringAsync();
            return html;
        }
    }


    /// <summary>
    /// Extract position
    /// </summary>
    /// <param name="estilo"></param>
    /// <returns></returns>
    static (int, int)? ExtractCoordenates(string estilo)
    {
        var match = Regex.Match(estilo, @"-?(\d+)px\s-?(\d+)px");
        if (match.Success)
        {
            int x = int.Parse(match.Groups[1].Value) * -1;
            int y = int.Parse(match.Groups[2].Value) * -1;
            return (x, y);
        }
        return null;
    }


    /// <summary>
    /// Calculate price
    /// </summary>
    /// <param name="y"></param>
    /// <param name="x"></param>
    /// <returns></returns>
    static int? CalcularNumeroDeSalida(int y, int x)
    {
        //data in positive
        y = y * -1;
        x = x * -1;

        //calculate
        int valorEntero = Math.Abs(y / -20); 
        double valorDecimal = Math.Abs(x / 40.0) * 0.01; 
        double resultadoFinal = valorEntero + valorDecimal;
        return (int)Math.Round(resultadoFinal * 100);
    }


    /// <summary>
    /// Export to csv
    /// </summary>
    /// <param name="datos"></param>
    /// <param name="nombreArchivo"></param>
    static void ExportarCsv(List<string[]> datos, string nombreArchivo)
    {
        using (var writer = new StreamWriter(nombreArchivo))
        {
            foreach (var fila in datos)
            {
                writer.WriteLine(string.Join(",", fila));
            }
        }
    }
}
