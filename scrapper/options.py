""" Definicion de línea de comando
"""
import gettext
from gettext import gettext as _
from scrapper.__version__  import VERSION
from scrapper.__version__  import NAME


gettext.textdomain('scrapper')

def _my_gettext(string):
    """Traducir algunas cadenas de argparse."""
    current_dict = {'usage: ': "uso: ",
                    'options': 'Opciones',
                    'optional arguments': 'Argumentos opcionales',
                    'show this help message and exit': 'Mostrar esta ayuda y salir',
                    'positional arguments': 'Argumentos posicionales',
                    'the following arguments are required: %s':
                            'los siguientes argumentos son requeridos: %s'}

    if string in current_dict:
        return current_dict[string]
    return string

gettext.gettext = _my_gettext

import argparse

def init_argparse():
    """Inicializar parametros del programa."""
    cmdparser = argparse.ArgumentParser(prog=NAME,
                                        #description="%s\n%s\n" % (DESCRIPTION, AUTHOR),
                                        epilog="",
                                        add_help=True,
                                        formatter_class=make_wide(argparse.HelpFormatter,
                                                                width=132,
                                                                height=80)
    )

    opciones = {    "proceso": {
                                "nargs": "?",
                                "default": None,
                                "help": _("Proceso de scrapping a utilizar")
                    },
                    "--version -v": {
                                "action":    "version",
                                "version":   VERSION,
                                "help":       _("Mostrar el número de versión y salir")
                    },
                    "---show-available-process -s": {
                                "default":    False,
                                "action":     "store_true",
                                "dest":       "show",
                                "help":       _("Mostrar los procesos disponibles")
                    },
                    "--log-level -n": {
                                "type":     str,
                                "action":   "store",
                                "dest":     "loglevel",
                                "default":  "info",
                                "help":     _("Nivel de log")
                    },
                    "--log-file -l": {
                            "type":	str,
                            "action": "store",
                            "dest":	"logfile",
                            "default": "",
                            "help":	_("Archivo de log"),
                            "metavar": "file"
                    },
                    "--input-param -p": {
                                "type":     str,
                                "action":   "store",
                                "dest":     "inputparam",
                                "default":   None,
                                "help":      _("Parametro variable de entrada")
                    },
                    "--input-file -i": {
                                "type":     str,
                                "action":   "store",
                                "dest":     "inputfile",
                                "default":   None,
                                "help":      _("Nombre del archivo de entrada de datos")
                    },
                    "--output-file -f": {
                                "type":     str,
                                "action":   "store",
                                "dest":     "outputfile",
                                "default":    None,
                                "help": _("Nombre del archivo de salida de los datos capturados")
                    },
                    "--output-type -t": {
                                "type":     str,
                                "action":   "store",
                                "dest":     "outputtype",
                                "default":  "None",
                                "help":     _("Formato de salida")
                    },
                     "--show-browser -b": {
                                "action":   "store_true",
                                "dest":     "show_browser",
                                "default":  False,
                                "help":     _("Muestra el navegador y la interacción")
                    },
                    "--quiet -q": {
                                "action":     "store_true",
                                "dest":     "quiet",
                                "default":    False,
                                "help": _("Modo silencioso sin mostrar los mensajes de progreso.")
                    },
                }

    for key, val in opciones.items():
        args = key.split()
        kwargs = {}
        kwargs.update(val)
        cmdparser.add_argument(*args, **kwargs)

    return cmdparser



def make_wide(formatter, width=120, height=40):
    """Return a wider HelpFormatter, if possible."""
    try:
        # https://stackoverflow.com/a/5464440
        # beware: "Only the name of this class is considered a public API."
        kwargs = {'width': width, 'max_help_position': height}
        formatter(None, **kwargs)
        return lambda prog: formatter(prog, **kwargs)
    except TypeError:
        print("argparse help formatter failed, falling back.")
        return formatter
