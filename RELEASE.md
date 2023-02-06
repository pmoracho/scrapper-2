# Descripción

* Implementamos salida a `CSV` con separador por `;`
* Validamos por firma que los archivos descargados sean `pdf`
* Incorporamos a modo de ejemplo camptura de datos de **zonaprop**

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

La salida en `resumen.csv` sería algo así:

    "20190103146";"EPA";"tmp/20190103146-EPA-1.pdf";"OK: Decarga exitosa"
    "20190103074";"Arxxxxxxx";"";"No se ha encontrado archivo en los primeros 10 resultados"
    "20190102902";"Titulo";"";"No se ha encontrado archivo en los primeros 10 resultados"
    "20190102881";"ACLARACION PREVIA";"tmp/20190102881-ACLARACION PREVIA-1.pdf";"OK: Decarga exitosa"
    "20190102794";"ACLARACION PREVIA";"tmp/20190102794-ACLARACION PREVIA-1.pdf";"OK: Decarga exitosa"
    "20190102793";"ACLARACION PREVIA";"tmp/20190102793-ACLARACION PREVIA-1.pdf";"OK: Decarga exitosa"
    "20190102675";"Examen de Fondo";"";"No se ha encontrado archivo en los primeros 10 resultados"
    "20190102351";"ACLARACION PREVIA";"";"No se ha encontrado archivo en los primeros 10 resultados"
    "20190102008";"ACLARACION PREVIA";"tmp/20190102008-ACLARACION PREVIA-1.pdf";"OK: Decarga exitosa"


# Detalle del `build`

* `python 3.10`
*  Build actions (de terceros):
   - pyinstaller: sayyid5416/pyinstaller@3f23c8bb6c4afd3f7886806e62baac781f468009
   - create release: softprops/action-gh-release@de2c0eb89ae2a093876385947365aca7b0e5f844

[chrome]: https://chromedriver.chromium.org/downloads