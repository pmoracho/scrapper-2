"""
patentes_inpi_novedades
"""
import os
import time
import shutil
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def is_a_pdf(filename):
    """Check if a PDF is a PDF
    """
    magic = bytes([0x25, 0x50, 0x44, 0x46])

    with open(filename, 'rb') as infile:
        file_head = infile.read(len(magic))

    return file_head.startswith(magic)


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

    def get_last_downloaded_file_path(dummy_dir, time_to_wait=30):
        """ Return the last modified -in this case last downloaded- file path.
            This function is going to loop as long as the directory is empty
            or reched a timeout
        """
        time_counter = 0

        while not [f for f in os.listdir(dummy_dir) if re.match(r'.*\.pdf', f)]:
            time.sleep(1)
            time_counter += 1
            if time_counter > time_to_wait:
                break

        return max([os.path.join(dummy_dir, f) for f in os.listdir(dummy_dir)],
                    key=os.path.getctime)

    def _get_solicitud_data(solicitud_a_buscar, tipo_doc):


        log.info(
            f"Procesando solicitud: {solicitud_a_buscar} tipo de documento: {tipo_doc}")
        url = parametros["url"]

        driver.get(url)

        txt_solicitud = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, parametros["txt_solicitud"]))
        )
        txt_solicitud.send_keys(solicitud_a_buscar)
        txt_solicitud.submit()

        btn_more = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, parametros["btn_more"]))
        )
        btn_more.click()

        label_grilla_digital = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.XPATH, parametros["label_grilla_digital"]))
        )
        label_grilla_digital.click()

        col = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.XPATH, parametros["grilla"] + "/tr[1]/td[3]"))
        )

        files = []
        for i in range(1, 11):
            col_tipo_doc_xpath = parametros["grilla"] + f"/tr[{i}]/td[3]"
            col = driver.find_element(By.XPATH, col_tipo_doc_xpath)
            # log.info(f"Texto encontrado {col.text}")
            if col.text == tipo_doc:
                descarga_xpath = parametros["grilla"] + f"/tr[{i}]/td[1]/a"
                log.debug(f"Descargando desde {descarga_xpath}")

                btn = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, descarga_xpath))
                )

                # file = btn.get_property("href").split("=")[2]
                btn.click()
                log.debug(
                    "Encontramos documento y hacemos click sobre el botón de descarga")

                latest_downloaded_filename = get_last_downloaded_file_path(
                    temp_download_folder)

                _, file_extension = os.path.splitext(
                    latest_downloaded_filename)


                nfile = len(files) + 1
                if latest_downloaded_filename:
                    new_file = os.path.join(
                        outputpath,
                        f"{solicitud_a_buscar}-{tipo_doc}-{nfile}{file_extension}"
                    )
                    shutil.move(latest_downloaded_filename, new_file)
                    log.info(f"Movemos {latest_downloaded_filename} a {new_file}")
                    files.append(os.path.join(new_file))
                else:
                    files = []

        return files

    log.info(f"Leyendo solicitudes desde: {inputfile}")
    temp_download_folder = os.path.join(outputpath, "tmp")

    solicitudes = []
    with open(inputfile, "r", encoding="utf-8") as infile:
        lineas_leidas = infile.readlines()
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
            if len(files) == 0:
                datos.append(
                    (solicitud_a_buscar,
                    tipo_doc,
                    None,
                    "No se ha encontrado archivo en la primer pagina de novedades")
                )
            else:
                for file in files:
                    log.info(f"archivo descargado y renombrado: {file}")
                    if is_a_pdf(file):
                        datos.append((solicitud_a_buscar, tipo_doc,
                                    file, "OK: Descarga exitosa"))
                    else:
                        datos.append((solicitud_a_buscar, tipo_doc,
                                    file, "ERROR: El archivo no es un PDF"))

        except Exception:
            log.exception(f"al procesar solicitud {solicitud_a_buscar}")
            datos.append((solicitud_a_buscar,
                          tipo_doc,
                          None,
                          "ERROR: No se ha podido procesar la solicitud"))

        i = i + 1

    driver.quit()

    return datos
