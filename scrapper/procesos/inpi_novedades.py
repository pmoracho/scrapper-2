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
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException

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
        while not any(os.path.isfile(os.path.join(dummy_dir, f)) and contains == f.lower()
                        for f in os.listdir(dummy_dir)) and elapsed_time < time_to_wait:
            # log.info_internal(f"contains: *{contains}*")
            # log.info_internal("Archivos:" + ", ".join(os.listdir(dummy_dir)))
            time.sleep(1)  # esperar 1 segundo
            elapsed_time += 1

        files = [os.path.join(dummy_dir, f) for f in os.listdir(dummy_dir) if contains == f.lower()]
        if len(files) > 0:
            if len(files) > 1:
                log.error("Se ha encontrado más de un archivo en la carpeta de descarga")

            log.info_internal("Archivos descargados:" + ",".join(files))

        if len(files) == 0:
            return None

        return max(files, key=os.path.getctime)

    def get_download_urls_list(rows):
        """get_download_urls_list
           Retorna una lista de los links de descarga de la tabla de notificaciones
           rows: lista de filas de la tabal de notificaciones
        """
        files = []
        for i, row in enumerate(rows, 1):

            cols = row.find_elements(By.TAG_NAME, "td")
            solicitud = cols[0].text
            tipo = cols[1].get_attribute("textContent")
            fecha = cols[3].text

            descarga_xpath = parametros["descarga"].replace("{id}", str(i))
            try:
                btn_decarga = WebDriverWait(driver, big_timeout).until(
                                    EC.element_to_be_clickable((By.XPATH, descarga_xpath))
                                )
                descarga = btn_decarga.get_attribute('download')
                url = btn_decarga.get_attribute('href')

            # pylint: disable=broad-exception-caught
            except Exception as err:
                log.exception(str(err))

            files.append((solicitud,
                        tipo,
                        fecha,
                        url,
                        descarga))

        return files

    def simulate_activity():
        try:
            btn_inicio = WebDriverWait(driver, small_timeout).until(
                EC.visibility_of_element_located(
                    (By.XPATH, parametros["inicio"]))
            )
            btn_inicio.click()
        except Exception as err:
            log.exception(str(err))

    def download_files(rows):
        """download_files
           Descarga archivos de una lista de norificaciones
        """
        temp_download_folder = os.path.join(outputpath, "tmp")
        files = [("Solicitud", "Tipo", "Fecha", "Archivo", "Estatus")]
        total = len(rows)

        for i, row in enumerate(rows, 1):

            solicitud, tipo, fecha, url, descarga = row
            new_file = None
            try:
                log.info_internal(f"Descargando desde: {url}")

                descarga_xpath = parametros["descarga"].replace("{id}", str(i))

                btn_decarga = WebDriverWait(driver, big_timeout).until(
                                    EC.element_to_be_clickable((By.XPATH, descarga_xpath))
                                )

                log.info_internal(f"Encontramos el botón de click de la fila {i}")
                try:
                    btn_decarga.click()
                except ElementClickInterceptedException:
                    btn_decarga = WebDriverWait(driver, big_timeout).until(
                                        EC.element_to_be_clickable((By.XPATH, descarga_xpath))
                                    )
                    btn_decarga.click()

                # driver.get(url)
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
                    log.info_internal(f"Movemos {latest_downloaded_filename} a {new_file}")
                    status = "Ok. Descarga exitosa."
                else:
                    status = "Error. No se pudo completar la descarga (1)"

            # pylint: disable=broad-exception-caught
            except Exception as err:
                log.exception(str(err))
                status = "Error. No se pudo completar la descarga (2)"

            log.info(f"[{i}/{total}] Solicitud: {solicitud} tipo: {tipo} Status: {status}")
            files.append((solicitud,
                            tipo,
                            fecha,
                            new_file,
                            status))

        return files

    def novedades(cuil_cuit,
                  password,
                  fecha_desde,
                  fecha_hasta,
                  expediente,
                  notificacion,
                  show_browser):
        """Recuperación de notificaciones del INPI

        Args:
            cuil_cuit (str): cuil/cuit de login de afip. Puede ser "".
            password (str): contraseña de acceso al afip. Puede ser "".
            fecha_desde (str): Fecha desde para la consulta de notificaciones
            fecha_hasta (str): Fecha hastapara la consulta de notificaciones
            expediente (str): Datos del tipo de expediente (* para todos)
            notificacion (str): Tipo de notificación. Corresponde al optin_value
                                   del combo, no la descripción. (* para todos)
            show_browser (bool): Se muestra el navegador durante el proceso.

        Returns:
            List: Lista de datos obtenidos, puede ser una lista vacía.
        """
        url = parametros["url_home"]
        log.info_internal(f"Get: {url}")
        driver.get(url)

        log.info_internal(parametros["btn_inicio_sesion"])
        btn_inicio = WebDriverWait(driver, small_timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH, parametros["btn_inicio_sesion"]))
        )
        btn_inicio.click()

        if cuil_cuit:
            log.info_internal("completamos usuario")
            txt_usuario = WebDriverWait(driver, small_timeout).until(
                EC.visibility_of_element_located(
                    (By.ID, parametros["txt_usuario"]))
            )
            txt_usuario.send_keys(cuil_cuit)
            txt_usuario.send_keys(Keys.RETURN)

        if password:
            log.info_internal("completamos contraseña")
            txt_password = WebDriverWait(driver, small_timeout).until(
                EC.visibility_of_element_located(
                    (By.ID, parametros["txt_password"]))
            )
            txt_password.send_keys(password)
            txt_password.send_keys(Keys.RETURN)
            log.info_internal("Realizamos login")

        log.info_internal("Cambiamos a MARVAL")
        btn_cambiar = WebDriverWait(driver, big_timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH, parametros["btn_cambiar"]))
        )
        btn_cambiar.click()

        if show_browser and (not password or not cuil_cuit):
            driver.minimize_window()

        log.info_internal("Vamos a la página de notificaciones")
        url = parametros["url_notificaciones"]

        driver.get(url)
        log.info_internal("Esperamos filtros de búsqueda")
        txt_desde = WebDriverWait(driver, big_timeout).until(
            EC.visibility_of_element_located(
                (By.ID, parametros["txt_desde_id"]))
        )

        txt_hasta = WebDriverWait(driver, big_timeout).until(
            EC.visibility_of_element_located(
                (By.ID, parametros["txt_hasta_id"]))
        )
        log.info_internal("Completamos fechas de busqueda")
        txt_desde.send_keys(fecha_desde)
        txt_hasta.send_keys(fecha_hasta)

        if expediente != "*":
            select = Select(driver.find_element("id", parametros["expediente_combo"]))
            select.select_by_visible_text(expediente)
            log.info_internal(f"Seteamos combo de expediente: {expediente}")

        if notificacion != "*":
            select = Select(driver.find_element("id", parametros["notificacion_combo"]))
            select.select_by_value(notificacion)
            log.info_internal(f"Seteamos combo de notificacion: {notificacion}")

        btn_buscar = WebDriverWait(driver, big_timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH, parametros["btn_buscar"]))
        )
        log.info_internal("Realizamos busqueda")
        btn_buscar.click()

        log.info_internal("Aguardamos por el falso paginador")
        _ = WebDriverWait(driver, big_timeout).until(
            EC.visibility_of_all_elements_located(
                (By.XPATH, parametros["paginador"]))
        )

        log.info_internal("Aguardamos por los datos")
        try:
            rows = WebDriverWait(driver, small_timeout).until(
                EC.visibility_of_all_elements_located(
                    (By.XPATH, parametros["grilla"]))
            )
        except TimeoutException:
            log.info("No se han encontrado resultados")
            return None

        datos = None
        number_of_rows = len(rows)
        log.info(f"Encontramos {number_of_rows} notificaciones")
        if number_of_rows > 0:
            links = get_download_urls_list(rows)
            datos = download_files(links)

        log.info_internal("Finalizamos proceso de novedades, datos: " + str(len(datos)))
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
        datos = novedades(cuil_cuit,
                          password,
                          fecha_desde,
                          fecha_hasta,
                          expediente,
                          notificacion,
                          show_browser)

    # pylint: disable=broad-exception-caught
    except Exception as err:
        log.exception(str(err))

    driver.quit()
    log.info_internal("Fin del proceso de descarga, retornamos los datos.")

    return datos
