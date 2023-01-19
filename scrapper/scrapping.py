"""Wrapper a los proceso de scrapping
"""
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from scrapper.procesos.patentes_inpi_novedades import patentes_inpi_novedades

def get_chrome_driver(download_folder, show=False):
    """Configura y retorna el driver chrome
    """

    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument("--window-size=1920,1080")

    if not show:
        chrome_options.add_argument('--headless')

    chrome_options.add_experimental_option('prefs',
                                            {'download.default_directory' : download_folder,
                                            'service_log_path' : download_folder,
                                            "directory_upgrade": True})

    return webdriver.Chrome(options=chrome_options)


def scrap(proceso,
          config,
          log,
          inputparam=None,
          inputfile=None,
          outputpath = None,
          show_browser=False):
    """Ejecución de un proceso de scrapping
    """
    datos = []

    if outputpath is None:
        workpath = tempfile.mkdtemp()
    else:
        workpath = outputpath

    driver = get_chrome_driver(download_folder=workpath, show=show_browser)

    section        = "proc:" + proceso
    function_name  = config[section]["function"]

    if function_name in globals():
        function = globals()[function_name]
        log.info(f"Invocando a: {function_name}")

        try:
            datos = function(driver=driver,
                            log=log,
                            parametros=config[section],
                            inputfile=inputfile,
                            tmpdir=workpath,
                            inputparam=inputparam,
                            outputpath=outputpath)

        except Exception:
            log.exception("ejecutar scrap()")

    else:
        log.error(f"proceso {function_name} no implementado")

    return datos