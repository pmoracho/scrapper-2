import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def dummy_download_file(driver,
                        parametros,
                        log,
                        inputfile=None,
                        tmpdir=os.getcwd(),
                        inputparam=None,
                        outputpath=None):
    """Descarga dummy de prueba
    """
    log.info(f"LDescarga dummy de un archivo en la carpeta {outputpath}")

    options = Options()
    options.add_experimental_option("prefs", {
        "download.default_directory": outputpath,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    driver = webdriver.Chrome(options=options)

    driver.get("http://speedtest.ftp.otenet.gr/files/test100k.db")
    time.sleep(5)  # Espera unos segundos para que el archivo termine de descargarse

    driver.quit()
