"""
patentes_inpi_novedades
"""
import os
import time
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from progressbar import ProgressBar
from progressbar import FormatLabel
from progressbar import Percentage
from progressbar import Bar
from progressbar import RotatingMarker
from progressbar import ETA

def patentes_inpi_novedades(driver,
                            parametros,
                            log,
                            inputfile=None,
                            tmpdir=os.getcwd(),
                            inputparam=None,
                            outputpath=None):

    """Descarga de archivos de novedades de patendes del INPI
    Parametros requeriods:

    inputfile: Archivo tipo csv con numero de solicitud y tipo de documento
    """

    def get_downloaded_filename(wait_time):

        file_name = None
        driver.execute_script("window.open()")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get('chrome://downloads')

        end_time = time.time() + wait_time
        while True:
            try:
                file_name = driver.execute_script("return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content  #file-link').text")
                if file_name:
                    break
            except Exception:
                pass

            time.sleep(1)
            if time.time() > end_time:
                break

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return file_name

    def _get_solicitud_data(solicitud_a_buscar, tipo_doc):

        log.info(f"Procesando solicitud: {solicitud_a_buscar} tipo de documento: {tipo_doc}")
        url = parametros["url"]

        driver.get(url)

        txt_solicitud = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, parametros["txt_solicitud"]))
        )
        txt_solicitud.send_keys(solicitud_a_buscar)
        txt_solicitud.submit()

        btn_more = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, parametros["btn_more"]))
        )
        btn_more.click()

        label_grilla_digital = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, parametros["label_grilla_digital"]))
        )
        label_grilla_digital.click()

        col  = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, parametros["grilla"] + "/tr[1]/td[3]"))
        )

        files = []
        for i in range(1,11):
            col_tipo_doc_xpath = parametros["grilla"] + f"/tr[{i}]/td[3]"
            col = driver.find_element(By.XPATH, col_tipo_doc_xpath)
            #log.info(f"Texto encontrado {col.text}")
            if col.text == tipo_doc:
                descarga_xpath = parametros["grilla"] + f"/tr[{i}]/td[1]/a"
                log.debug(f"Descargando desde {descarga_xpath}")

                btn  = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH, descarga_xpath))
                )

                btn.click()
                log.info("click sobre el botón de descarga")

                latest_downloaded_filename = get_downloaded_filename(60)
                if latest_downloaded_filename:
                    files.append(os.path.join(outputpath, latest_downloaded_filename))
                else:
                    files = []

        return files

    log.info(f"Leyendo solicitudes desde: {inputfile}")
    solicitudes = []
    with open(inputfile, "r", encoding="utf-8") as f:
        lineas_leidas = f.readlines()
        for linea in lineas_leidas:
            if not linea.startswith("#"):
                solicitud, tipo_doc = linea.split(';')
                solicitudes.append((solicitud, tipo_doc.strip()))

    datos = [('Solicitud', 'Documento', 'Path', 'Estatus')]
    i = 1
    for fila in solicitudes:
        solicitud_a_buscar = fila[0]
        tipo_doc = fila[1]

        try:
            files = _get_solicitud_data(solicitud_a_buscar, tipo_doc)
            for file in files:
                datos.append((solicitud_a_buscar, tipo_doc, file, "OK: Decarga exitosa"))

        except Exception:
            log.exception(f"procesar solicitud {solicitud_a_buscar}")
            datos.append((solicitud_a_buscar,
                          tipo_doc,
                          None,
                          "ERROR: No se ha podido procesar la solicitud"))

        i = i + 1

    driver.quit()

    return datos
