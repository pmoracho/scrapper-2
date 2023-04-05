"""
inpi_novedades
"""
import os
import time
import shutil

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def inpi_novedades(driver,
                parametros,
                log,
                inputfile=None,
                tmpdir=os.getcwd(),
                inputparam=None,
                outputpath=None,
                show_browser=False):
    """Descarga de archivos de novedades del INPI
    Parametros requeriod0s:

    iputparam: <cuit/cuil>|<password>|<fecha_desde>|<fecha_hasta>
    """

    def get_last_downloaded_file_path(dummy_dir, contains="pdf", time_to_wait=50):
        """ Return the last modified -in this case last downloaded- file path.
            This function is going to loop as long as the directory is empty
            or reched a timeout
        """
        elapsed_time = 0
        contains = contains.lower()
        while not any(os.path.isfile(os.path.join(dummy_dir, f)) and contains == f.lower() for f in os.listdir(dummy_dir)) and elapsed_time < time_to_wait:
            log.debug(f"contains: *{contains}*")
            log.debug("Archivos:" + ", ".join(os.listdir(dummy_dir)))
            time.sleep(1)  # esperar 1 segundo
            elapsed_time += 1

        files = [os.path.join(dummy_dir, f) for f in os.listdir(dummy_dir) if contains == f.lower()]
        if len(files) > 0:
            if len(files) > 1:
                log.error("Se ha encontrado más de un archivo en la carpeta de descarga")

            log.debug("Archivos descargados:" + ",".join(files))

        if len(files) == 0:
            return None

        return max(files, key=os.path.getctime)

    def _download_files(rows):

        temp_download_folder = os.path.join(outputpath, "tmp")
        files = [("Solicitud", "Tipo", "Fecha", "Archivo", "Estatus")]
        total = len(rows)

        for i, row in enumerate(rows, 1):

            cols = row.find_elements(By.TAG_NAME, "td")
            solicitud = cols[0].text
            tipo = cols[1].get_attribute("textContent")
            fecha = cols[3].text

            log.info(f"[{i}/{total}] Solicitud: {solicitud} tipo: {tipo}")
            new_file = None
            try:

                a = cols[4].find_element(By.TAG_NAME, "a")
                descarga = a.get_attribute('download')
                a.click()
                log.debug(f"Click de la descarga, se espera el archivo: {descarga}")
                latest_downloaded_filename = get_last_downloaded_file_path(
                    temp_download_folder,
                    descarga,
                    big_timeout)

                if latest_downloaded_filename:
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
                else:
                    files.append((solicitud,
                                tipo,
                                fecha,
                                new_file,
                                "Error. No se pudo completar la descarga"))


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

        log.debug(parametros["btn_inicio_sesion"])
        btn_inicio = WebDriverWait(driver, small_timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH, parametros["btn_inicio_sesion"]))
        )
        btn_inicio.click()

        if cuil_cuit:
            log.debug("completamos usuario")
            txt_usuario = WebDriverWait(driver, small_timeout).until(
                EC.visibility_of_element_located(
                    (By.ID, parametros["txt_usuario"]))
            )
            txt_usuario.send_keys(cuil_cuit)
            txt_usuario.send_keys(Keys.RETURN)

        if password:
            log.debug("completamos contraseña")
            txt_password = WebDriverWait(driver, small_timeout).until(
                EC.visibility_of_element_located(
                    (By.ID, parametros["txt_password"]))
            )
            txt_password.send_keys(password)
            txt_password.send_keys(Keys.RETURN)
            log.debug("Realizamos login")

        log.debug("Cambiamos a MARVAL")
        btn_cambiar = WebDriverWait(driver, big_timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH, parametros["btn_cambiar"]))
        )
        btn_cambiar.click()

        driver.minimize_window()

        log.debug("Vamos a la página de notificaciones")
        url = parametros["url_notificaciones"]
        driver.get(url)

        txt_desde = WebDriverWait(driver, big_timeout).until(
            EC.visibility_of_element_located(
                (By.ID, parametros["txt_desde_id"]))
        )

        txt_hasta = WebDriverWait(driver, big_timeout).until(
            EC.visibility_of_element_located(
                (By.ID, parametros["txt_hasta_id"]))
        )
        log.debug("Completamos fechas de busqueda")
        txt_desde.send_keys(fecha_desde)
        txt_hasta.send_keys(fecha_hasta)

        if expediente != "*":
            select = Select(driver.find_element("id", parametros["expediente_combo"]))
            select.select_by_visible_text(expediente)

        if notificacion != "*":
            select = Select(driver.find_element("id", parametros["notificacion_combo"]))
            select.select_by_visible_text(notificacion)

        btn_buscar = WebDriverWait(driver, big_timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH, parametros["btn_buscar"]))
        )
        log.debug("Realizamos busqueda")
        btn_buscar.click()

        rows = WebDriverWait(driver, big_timeout).until(
            EC.visibility_of_all_elements_located(
                (By.XPATH, parametros["grilla"]))
        )

        datos = None
        number_of_rows = len(rows)
        log.info(f"Encontramos {number_of_rows} notificaciones")
        if number_of_rows > 0:
            datos = _download_files(rows)

        return datos

    big_timeout =int(parametros["big_timeout"])
    small_timeout =int(parametros["small_timeout"])

    cuil_cuit, password, fecha_desde, fecha_hasta, expediente, notificacion = inputparam.split("|")
    if (cuil_cuit == "" or password == "") and show_browser is False:
        raise AttributeError(
            "Si no se indican las credenciales de login la ejecución debe ser interactiva (-b)"
        )

    log.info(f"Leyendo {expediente}-{notificacion} desde: {fecha_desde} hasta {fecha_hasta}")

    datos = None
    try:
        datos = _novedades()
    # pylint: disable=broad-exception-caught
    except Exception as err:
        log.exception(str(err))

    driver.quit()
    log.debug("Fin del proceso de descarga, retornamos los datos.")

    return datos
