"""Test de la clase Config
"""
import os
import sys
import tempfile

from scrapper.config import Config

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_config():
    """Test de la lectura de una configuración
    """

    # Convert text into tmp file
    tmp_file = tempfile.NamedTemporaryFile(suffix=".cfg", delete=False)
    s_config = """
[general]
booleano = "True"
lista_cadenas = jpg, png, tif
lista_enteros = 1, 2, 3
float = 100.90
entero = 2
cadena = epa
otracosa = 1
"""
    with open(tmp_file.name, "w", encoding="utf-8") as inputfile:
        inputfile.write(s_config)

    cfg = Config(tmp_file.name)

    # pylint: disable=no-member
    assert cfg.booleano is True
    assert cfg.float == 100.9
    assert cfg.lista_cadenas == ['jpg', 'png', 'tif']
    assert cfg.lista_enteros == [1, 2, 3]
    assert cfg.entero == 2
    assert cfg.cadena == "epa"
