from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import xml.etree.ElementTree as ET
import os
import time
from pprint import pprint
import glob

def zonaprop(driver,
            parametros,
            log,
            inputfile=None,
            tmpdir=os.getcwd(),
            inputparam=None,
            outputpath=None,
            show_browser=False):

    def _get_element(xpath):
        try:
            return driver.find_element_by_xpath(xpath).text
        except Exception:
            return ""

    def _get_dat_from_ul(xpath):
        try:
            d = {
                "ambientes": None,
                "baños": None,
                "antiguedad": None,
                "superficie": None,
                "superficie_cubierta": None,
                "cochera": "No",
                "toilette": "No",
            }
            print(xpath)
            ul_item = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            options = driver.find_elements_by_css_selector("li")
            for option in options:
                print(option.text)

            print([el.text for el in ul_item.find_elements_by_tag_name("li")])

            for text in [el.text for el in ul_item.find_elements_by_tag_name("li")]:
                print(text)
                if "Ambientes" in text:
                    d["ambientes"] = text.split(" ")[0]
                if "Baños" in text:
                    d["baños"] = text.split(" ")[0]
                if "Antigüedad" in text:
                    d["antiguedad"] = text.split(" ")[0]
                if "Total" in text:
                    d["superficie"] = text.split(" ")[0]
                if "Cubierta" in text:
                    d["superficie_cubierta"] = text.split(" ")[0]
                if "Cochera" in text:
                    d["cochera"] = "Si"
                if "Toilette" in text:
                    d["toilette"] = "Si"
            return d

        except Exception:
            return {}

    def _get_propiedad_data(url_propiedad):

        driver.get(url_propiedad)

        precio = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, parametros["precio_xpath"]))
        )
        log.info(precio.text)
        expensas = "'" + _get_element(parametros["expensas_xpath"])
        decripcion = _get_element(parametros["descripcion_xpath"])

        datos = _get_dat_from_ul(parametros["datos_ul_xpath"])

        print(datos)

        mts_totales = datos["superficie"]
        mts_cubiertos = datos["superficie_cubierta"]
        ambientes = datos["ambientes"]
        banios = datos["baños"]
        cochera = datos["cochera"]
        toilette = datos["toilette"]
        antiguedad = datos["antiguedad"]

        direccion = _get_element(parametros["dir_xpath"])
        publicado = _get_element(parametros["publicado_xpath"])
        inmobiliaria = _get_element(parametros["inmobiliaria_xpath"])

        return (
            decripcion,
            direccion.replace('\r', '').replace('\n', '').replace('Ver en mapa', ''),
            precio.text,
            expensas,
            mts_totales,
            mts_cubiertos,
            ambientes,
            banios,
            toilette,
            cochera,
            antiguedad,
            publicado,
            inmobiliaria,
            url_propiedad,
        )

    datos = [('Detalle', 'Dirección', 'Precio', 'Expensas', 'Mts Totales', 'Mts Cubiertos',
            'Ambientes', 'Baños', 'Toilette', 'Cochera',
            'Antiguedad', 'Publicado', 'Inmobiliaria', 'URL')]

    urls = list()

    if inputparam is not None:
        urls = [inputparam]
    else:
        with open(inputfile, "r", encoding="utf-8") as f:
            urls = f.readlines()


    i = 1
    for url_propiedad in urls:
        url_propiedad = url_propiedad.strip()

        try:
            # a = 1/0
            datos.append(_get_propiedad_data(url_propiedad))
        except Exception as err:

            vacio = list("" for _ in range(len(datos[0])))
            vacio[-1] = "!!!Error: {0}".format(err)
            datos.append(tuple(vacio))

        i = i + 1


    driver.quit()

    return datos

