# Descripción

* Implementamos salida `CSV`

# Despliegue

* Descargar `win_release.zip` o `linux_release.zip`
* Descomprimir el contenido, se genera una carpeta `scrapper`
* La versión para `linux` puede que requiera hacer: `cd scrapper;chmod +x scrapper`
* **Importante**:
    - descargar driver chrome desde [aqui][chrome] 
    - Solo si en el equipo ya tenemos un navegador chrome, buscar el driver que
    coincida con la versión del primero. 
    - Descomprimir el ejecutable en la misma carpeta de `scrapper`


# Ejecución

## Para la captrua de novedades del **INPI**

Se necesita un archivo `csv` (separado por `;`) con los siguentes datos:

* Número de solicitud
* Nombre del documento (tal como aparece en la página)

Además se debe contar con una carpeta vacía dónde descargar los archivos y el
resumen. La ejecución sería algo así: 

    scrapper patentes_inpi_novedades -i ejemplo_solicitudes.txt -o tmp/ -f resumen.csv -t csv


[chrome]: https://chromedriver.chromium.org/downloads