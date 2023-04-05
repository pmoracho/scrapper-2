import time
import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_last_downloaded_file_path(dummy_dir, extension="pdf", time_to_wait=30):
    """ Return the last modified -in this case last downloaded- file path.
        This function is going to loop as long as the directory is empty
        or reched a timeout
    """
    elapsed_time = 0

    while not any(os.path.isfile(os.path.join(dummy_dir, f)) and extension in f for f in os.listdir(dummy_dir)) and elapsed_time < time_to_wait:
        time.sleep(1)  # esperar 1 segundo
        elapsed_time += 1

    return max([os.path.join(dummy_dir, f) for f in os.listdir(dummy_dir)],
                key=os.path.getctime)


def dummy_download_file(driver,
                        parametros,
                        log,
                        inputfile=None,
                        tmpdir=os.getcwd(),
                        inputparam=None,
                        outputpath=None,
                        show_browser=False):
    """Descarga dummy de prueba
    """
    log.info(f"Descarga dummy de un archivo en la carpeta {outputpath}")

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument(f"--download-directory={outputpath}")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--window-size=1920,1080")
    options.add_experimental_option("prefs", {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "download.default_directory": outputpath,
        "safebrowsing.enabled": True,
        'safebrowsing.disable_download_protection': True
    })


    driver = webdriver.Chrome(options=options)

    driver.get("http://speedtest.ftp.otenet.gr/files/test100k.db")

    log.info("Esperamos hasta 30 segundos")
    latest_downloaded_filename = get_last_downloaded_file_path(
                        outputpath
    )

    log.info(f"Descargamos {latest_downloaded_filename}")
    driver.quit()
