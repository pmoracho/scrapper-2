"""
inpi_novedades
"""
import os
import time
import shutil

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def inpi_novedades(driver,
                parametros,
                log,
                inputfile=None,
                tmpdir=os.getcwd(),
                inputparam=None,
                outputpath=None):
    """Descarga de archivos de novedades del INPI
    Parametros requeriod0s:

    iputparam: <cuit/cuil>|<password>|<fecha_desde>|<fecha_hasta>
    """

    def get_last_downloaded_file_path(dummy_dir, extension="pdf", time_to_wait=30):
        """ Return the last modified -in this case last downloaded- file path.
            This function is going to loop as long as the directory is empty
            or reched a timeout
        """
        elapsed_time = 0
        while not any(os.path.isfile(os.path.join(dummy_dir, f)) and extension in f for f in os.listdir(dummy_dir)) and elapsed_time < time_to_wait:
            time.sleep(1)  # esperar 1 segundo
            elapsed_time += 1

        files = os.listdir(dummy_dir)
        if len(files) == 0:
            return None

        return max([os.path.join(dummy_dir, f) for f in files],
                    key=os.path.getctime)

    def _download_files(rows):

        temp_download_folder = os.path.join(outputpath, "tmp")
        files = []
        for row in rows:

            cols = row.find_elements(By.TAG_NAME, "td")
            solicitud = cols[0].text
            tipo = cols[1].get_attribute("textContent")
            fecha = cols[3].text

            log.info(f"Solicitud: {solicitud} tipo: {tipo}")

            cols[4].click()

            log.debug(
                    "Encontramos documento y hacemos click sobre el botón de descarga")

            try:
                latest_downloaded_filename = get_last_downloaded_file_path(
                    temp_download_folder)
                _, file_extension = os.path.splitext(
                    latest_downloaded_filename)

                new_file = os.path.join(
                    outputpath,
                    f"{solicitud}-{tipo}{file_extension}"
                )
                shutil.move(latest_downloaded_filename, new_file)
                log.debug(f"Movemos {latest_downloaded_filename} a {new_file}")
                files.append((solicitud,
                              tipo,
                              fecha,
                              new_file,
                              "Ok. Descarga exitosa."))

            # pylint: disable=broad-exception-caught
            except Exception as err:

                files.append((solicitud,
                              tipo,
                              fecha,
                              new_file,
                              "Error." + str(err)))

        return files


    def _novedades():
        """Recuperación de notificaciones del INPI por fecha
        """

        url = parametros["url_home"]
        log.debug(f"Get: {url}")
        driver.get(url)
        datos = ["Solicitud", "Tipo", "Fecha", "Archivo", "Estatus"]

        log.debug(parametros["btn_inicio_sesion"])
        btn_inicio = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, parametros["btn_inicio_sesion"]))
        )
        btn_inicio.click()

        log.debug("completamos usuario")
        txt_usuario = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.ID, parametros["txt_usuario"]))
        )
        txt_usuario.send_keys(cuil_cuit)
        txt_usuario.send_keys(Keys.RETURN)

        log.debug("completamos contraseña")
        txt_password = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.ID, parametros["txt_password"]))
        )
        txt_password.send_keys(password)
        txt_password.send_keys(Keys.RETURN)
        log.debug("Realizamos login")

        log.debug("Cambiamos a MARVAL")
        btn_cambiar = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, parametros["btn_cambiar"]))
        )
        btn_cambiar.click()

        log.debug("Vamos a la página de notificaciones")
        url = parametros["url_notificaciones"]
        driver.get(url)

        txt_desde = WebDriverWait(driver, 50).until(
            EC.visibility_of_element_located(
                (By.ID, parametros["txt_desde_id"]))
        )

        txt_hasta = WebDriverWait(driver, 50).until(
            EC.visibility_of_element_located(
                (By.ID, parametros["txt_hasta_id"]))
        )
        log.debug("Completamos fechas de busqueda")
        txt_desde.send_keys(fecha_desde)
        txt_hasta.send_keys(fecha_hasta)

        btn_buscar = WebDriverWait(driver, 50).until(
            EC.visibility_of_element_located(
                (By.XPATH, parametros["btn_buscar"]))
        )
        log.debug("Realizamos busqueda")
        btn_buscar.click()

        rows = WebDriverWait(driver, 50).until(
            EC.visibility_of_all_elements_located(
                (By.XPATH, parametros["grilla"]))
        )

        number_of_rows = len(rows)
        log.info(f"Encontramos {number_of_rows} notificaciones")
        if number_of_rows > 0:
            datos = _download_files(rows)

        return datos

    cuil_cuit, password, fecha_desde, fecha_hasta = inputparam.split("|")
    log.info(f"Leyendo novedades desde: {fecha_desde} hasta {fecha_hasta}")

    datos = _novedades()
    driver.quit()
    log.debug("Fin del proceso de descarga, retornamos los datos.")

    return datos
