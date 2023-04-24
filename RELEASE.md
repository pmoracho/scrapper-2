# Descripción

`inpi_novedades`:

* Modificamos estrategia de carga de páginas para optimizar tiempos,
  particularmente con la carga inicial de cada url, dejamos de esperar
  la carga completa.
* Simulamos actividad cada 3 descargas para evitar fin de sesión
* Mejoramos los tiempos cuando debemos detectar que no hay resultados
* Mejora en el Log, más detalle sin necesidad de usar el modo debug
* Agregamos espera a que cada botón de descarga sea clickeable

[Notas](doc/Notas.md)

# Despliegue

* Requerimiento inicial: Tener instalado un navegador **Chrome**
* Descargar `win_release.zip`
* Descomprimir el contenido, se genera una carpeta `scrapper`
* **Importante**:
    - descargar driver chrome desde [aqui][chrome] (verificar que la versión sea consistente con la del navegador)
    - Solo si en el equipo ya tenemos un navegador chrome, buscar el driver que
      coincida con la versión del primero.
    - Descomprimir el ejecutable en la misma carpeta de `scrapper`


# Ejecución

## Para la captura de notificaciones del **INPI**

Se necesita indicar los siguientes parámetros:

Para el login mediante AFIP:

* cuit/cuil
* contraseña

En caso de no querer pasar estos datos, dejar en blanco los mismos, y se deberá
ingresar estos de forma manual en el navegador.

Para la consulta:

* fecha desde: formato `DD/MM/YYYY`
* fecha hasta: formato `DD/MM/YYYY`
* expediente: tal como figura el dropbox del la página, eventualmente "*" = todos
* tipo de notificacion: tal como figura el `option_value` del dropbox del la página,
  eventualmente "*" = todos o por ejemplo `4177` para `CONFIRMACIÓN DE ENVÍO`


Además se debería contar con una carpeta vacía dónde generar el resumen de la
operación que luego se puede importar para ubicar los archivos descargados o el
error al intentarlo.

La ejecución sería algo así:

    scrapper inpi_novedades -p "cuil/cuit|contraseña|fecha desde|fecha hasta|*|*" -f carpeta_accesible_por_mecanus\resumen.csv -t csv -l carpeta_accesible_por_mecanus\scrapper.log

O bien, sin pasar credenciales:

    scrapper inpi_novedades -p "||fecha desde|fecha hasta|*|*" -f carpeta_accesible_por_mecanus\resumen.csv -t csv -l carpeta_accesible_por_mecanus\scrapper.log

La salida en `resumen.csv` sería algo así:

    "4215067";"Boletin de Marcas";"10/03/2023 06:01:50 a.m.";"/home/pmoracho/Proyectos/scrapper-2/tmp/4215067-Boletin de Marcas.pdf";"Ok. Descarga exitosa."
    "4214712";"Boletin de Marcas";"10/03/2023 06:01:50 a.m.";"/home/pmoracho/Proyectos/scrapper-2/tmp/4214712-Boletin de Marcas.pdf";"Ok. Descarga exitosa."
    "4214711";"Boletin de Marcas";"10/03/2023 06:01:50 a.m.";"/home/pmoracho/Proyectos/scrapper-2/tmp/4214711-Boletin de Marcas.pdf";"Ok. Descarga exitosa."
    "4214710";"Boletin de Marcas";"10/03/2023 06:01:50 a.m.";"/home/pmoracho/Proyectos/scrapper-2/tmp/4214710-Boletin de Marcas.pdf";"Ok. Descarga exitosa."
    "4214709";"Boletin de Marcas";"10/03/2023 06:01:50 a.m.";"/home/pmoracho/Proyectos/scrapper-2/tmp/4214709-Boletin de Marcas.pdf";"Ok. Descarga exitosa."
    "4214708";"Boletin de Marcas";"10/03/2023 06:01:50 a.m.";"/home/pmoracho/Proyectos/scrapper-2/tmp/4214708-Boletin de Marcas.pdf";"Ok. Descarga exitosa."
    "4213559";"Boletin de Marcas";"10/03/2023 06:01:50 a.m.";"/home/pmoracho/Proyectos/scrapper-2/tmp/4213559-Boletin de Marcas.pdf";"Ok. Descarga exitosa."
    "4213558";"Boletin de Marcas";"10/03/2023 06:01:50 a.m.";"/home/pmoracho/Proyectos/scrapper-2/tmp/4213558-Boletin de Marcas.pdf";"Ok. Descarga exitosa."
    "4213557";"Boletin de Marcas";"10/03/2023 06:01:50 a.m.";"/home/pmoracho/Proyectos/scrapper-2/tmp/4213557-Boletin de Marcas.pdf";"Ok. Descarga exitosa."
    "4213556";"Boletin de Marcas";"10/03/2023 06:01:50 a.m.";"/home/pmoracho/Proyectos/scrapper-2/tmp/4213556-Boletin de Marcas.pdf";"Ok. Descarga exitosa."
    "4213554";"Boletin de Marcas";"10/03/2023 06:01:50 a.m.";"/home/pmoracho/Proyectos/scrapper-2/tmp/4213554-Boletin de Marcas.pdf";"Ok. Descarga exitosa."
    "4213553";"Boletin de Marcas";"10/03/2023 06:01:50 a.m.";"/home/pmoracho/Proyectos/scrapper-2/tmp/4213553-Boletin de Marcas.pdf";"Ok. Descarga exitosa."
    "4213551";"Boletin de Marcas";"10/03/2023 06:01:50 a.m.";"/home/pmoracho/Proyectos/scrapper-2/tmp/4213551-Boletin de Marcas.pdf";"Ok. Descarga exitosa."
    "4213550";"Boletin de Marcas";"10/03/2023 06:01:50 a.m.";"/home/pmoracho/Proyectos/scrapper-2/tmp/4213550-Boletin de Marcas.pdf";"Ok. Descarga exitosa."
    "4213543";"Boletin de Marcas";"10/03/2023 06:01:50 a.m.";"/home/pmoracho/Proyectos/scrapper-2/tmp/4213543-Boletin de Marcas.pdf";"Ok. Descarga exitosa."

**Importante**

* Crear previamente una carpeta vacía dónde salvar la descarga y los resultados
* Esto `-f carpeta_accesible_por_mecanus\resumen.csv` configura:
    - Dónde se salvan el archivo con el resumen del proceso
    - Los archivos descargados



# Detalle del `build`

* `python 3.10`
*  Build actions (de terceros):
   - pyinstaller: sayyid5416/pyinstaller@3f23c8bb6c4afd3f7886806e62baac781f468009
   - create release: softprops/action-gh-release@de2c0eb89ae2a093876385947365aca7b0e5f844

[chrome]: https://chromedriver.chromium.org/downloads