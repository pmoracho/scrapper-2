"""Wrapper a los proceso de scrapping
"""
import tempfile
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



# pylint: disable=unused-import
from scrapper.procesos.patentes_inpi_novedades import patentes_inpi_novedades
from scrapper.procesos.zonaprop import zonaprop
from scrapper.procesos.dummy import dummy_download_file
from scrapper.procesos.inpi_novedades import inpi_novedades

def get_chrome_driver(download_folder, show=False):
    """Configura y retorna el driver chrome

    Args:
        download_folder (str): Carpeta de descarga deseada
        show (bool): Establece si se muestra la operación en el navegador

    Returns:
        driver: retorna el objeto driver
    """

    chrome_options = Options()
    if not show:
        chrome_options.add_argument("--headless=new")

    chrome_options.add_argument(f"--download-directory={download_folder}")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("prefs", {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "download.default_directory": download_folder,
        "safebrowsing.enabled": True,
        'safebrowsing.disable_download_protection': True
    })
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    caps = DesiredCapabilities().CHROME
    #caps["pageLoadStrategy"] = "normal"  #  complete
    #caps["pageLoadStrategy"] = "eager"  #  interactive
    caps["pageLoadStrategy"] = "none"

    driver = webdriver.Chrome(options=chrome_options, desired_capabilities=caps)

    return driver


def scrap(proceso,
          config,
          log,
          inputparam=None,
          inputfile=None,
          outputpath = None,
          show_browser=False):
    """Ejecución generica de un proceso  modelo de scrapping

    Args:
        proceso (str): Nombre del proceps
        config (Config): Objeto de Configuración
        log (Log): Objeto de Logging
        inputparam (str, optional): Cadena variable de parámetros dada por el usuario.
                                    Defaults to None.
        inputfile (str, optional): Archivo de entrada. Defaults to None.
        outputpath (str, optional): Carpeta de salida de los resultados. Defaults to None.
        show_browser (bool, optional): Se muestra muestra el navegador durante el proceso
                                       de scrapping.
                                       Defaults to False.

    Returns:
        List: Lista de valores capturados
    """

    if outputpath is None:
        workpath = tempfile.mkdtemp()
    else:
        workpath = outputpath

    temp_download_folder = os.path.join(workpath, "tmp")
    os.makedirs(temp_download_folder, exist_ok=True)

    log.info(f"Carpeta de descarga: {temp_download_folder}")
    driver = get_chrome_driver(download_folder=temp_download_folder, show=show_browser)

    section         = "proc:" + proceso
    function_name   = config[section]["function"]
    datos           = []
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
                            outputpath=outputpath,
                            show_browser = show_browser)

        # pylint: disable=broad-except
        except Exception as err:
            log.exception("General en la invocación a la función de scrapping")
            log.exception(str(err))

    else:
        log.error(f"proceso {function_name} no implementado")

    return datos
