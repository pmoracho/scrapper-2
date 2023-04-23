"""Manejo de configuraciones
"""
import os
import sys
from configparser import ConfigParser
from pydoc import locate

def _find_real_path_for_cfgfile(file):
    """Buscamos el path dónde podría estar el archivo de configuración
    """
    application_path = None
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)

    cfgfile = os.path.join(application_path, file)
    if not os.path.isfile(cfgfile):
        cfgfile = os.path.join(application_path, "../", file)

    cfgfile = os.path.abspath(cfgfile)
    return cfgfile

# pylint: disable=too-few-public-methods
class Config:
    """Clase para manejo de configuración tipo INI
    """

    DEF_CFG = {"lista_cadenas": ["jpg"],
               "lista_enteros": [20, 20, 20, 20],
               "float": 1.0,
               "entero": 150,
               "booleano": False,
               "cadena": '',
               "progress_bar_ticks": 20,
            }

    def __init__(self, file=None, override_section=None):

        self.config = ConfigParser()
        self.__dict__.update(self.DEF_CFG)

        self.cfgfile = None if file is None else _find_real_path_for_cfgfile(file)
        self.file = self.cfgfile
        self.override_section = override_section

        if self.file:
            if isinstance(self.file, str):
                # pylint: disable=consider-using-with
                self.file = open(self.file, "rt", encoding="utf-8")

            self._load('general')
            if self.override_section:
                self._load(self.override_section)

    def _load(self, section):
        """Carga en memoria una sección del archivo de configuración

        Args:
            section (str): Nombre de la seció
        """
        self.config.read_file(self.file)
        items_ini = self.config.items(section)

        for (k, value) in items_ini:

            if k in self.__dict__:
                dct = self.__dict__[k]
                if isinstance(dct, list):
                    first = dct[0]
                    self.__dict__[k] = list(map(locate(type(first).__name__),
                                                [x.strip() for x in value.split(',')]))
                else:
                    self.__dict__[k] = locate(type(dct).__name__)(value)

    def __str__(self):
        # pylint: disable=no-member
        return f"""
-------------- Config -------------------
lista_cadenas: {self.lista_cadenas}
lista_enteros: {self.lista_enteros}
        float: {self.float}
       entero: {self.entero}
     booleano: {self.booleano}
       cadena: {self.cadena}
-----------------------------------------
      """
