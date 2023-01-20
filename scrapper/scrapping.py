"""Wrapper a los proceso de scrapping
"""
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from scrapper.procesos.patentes_inpi_novedades import patentes_inpi_novedades

def enable_download_in_headless_chrome(driver, download_dir):
    """
    there is currently a "feature" in chrome where
    headless does not allow file download: https://bugs.chromium.org/p/chromium/issues/detail?id=696481
    This method is a hacky work-around until the official chromedriver support for this.
    Requires chrome version 62.0.3196.0 or above.
    """

    # add missing support for chrome "send_command"  to selenium webdriver
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    command_result = driver.execute("send_command", params)


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
        chrome_options.add_argument('--headless=chrome')

    chrome_options.add_experimental_option('prefs',
                                            {'download.default_directory' : download_folder,
                                            'service_log_path' : download_folder,
                                            "download.prompt_for_download": False,
                                            "directory_upgrade": True,
                                            'safebrowsing.enabled': False,
                                            'safebrowsing.disable_download_protection': True
                                            })

    driver = webdriver.Chrome(options=chrome_options)
    #enable_download_in_headless_chrome(driver, download_folder)

    return driver


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
            log.exception("al ejecutar scrap()")

    else:
        log.error(f"proceso {function_name} no implementado")

    return datos