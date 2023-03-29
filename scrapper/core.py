#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2014 Patricio Moracho <pmoracho@gmail.com>
#
# scrapper.py
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 3 of the GNU General Public License
# as published by the Free Software Foundation. A copy of this license should
# be included in the file GPL-3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

"""
scrapper
========

Herramienta de línea de comandos para extracción de datos de páginas útiles

"""
import sys
import time
import tempfile
import os

try:
    from scrapper.__version__  import NAME
    from scrapper.__version__  import DESCRIPTION
    from scrapper.__version__  import VERSION
    from scrapper.__version__  import TITLE
    from scrapper.options import init_argparse
    from scrapper.log import Log
    from scrapper.config import Config
    from scrapper.tabulate import tabulate
    from scrapper.scrapping import scrap

except ImportError as err:
    modulename = err.args[0].partition("'")[-1].rpartition("'")[0]
    print(f"No fue posible importar el modulo: {modulename}")
    sys.exit()

def sum_function_to_test(op1, op2):
    """Una función de ejemplo"""
    return op1 + op2

def show_procs(available_data):
    """Muestra los procesos disponibles"""
    tablestr = tabulate(
                    tabular_data        = available_data,
                    headers             = ["Proceso", "Descripción" ],
                    tablefmt            = "psql",
                    stralign            = "left"
        )

    print("\nProcesos disponibles:")
    print(tablestr)

def return_datos(log,
                 outputfile,
                 outputtype,
                 datos):
    """Retorna los datos capturados
    """
    registros = datos[1:]
    header_row = datos[0]

    if outputtype == "transpose":
        registros = []
        maxlen = len(max(header_row, key=len))
        for fila in datos[1:]:
            for idx, header_col in enumerate(header_row, 0):
                registros.append([header_col, fila[idx]])

                lng = max(str(len(c)) for c in fila)
                maxlen = max(maxlen, lng)

        header_row = ["Campo", "Valor"]

    tablestr = tabulate(
        tabular_data        = registros,
        headers             = [] if outputtype == "csv" else header_row,
        tablefmt            = outputtype,
        stralign            = None if outputtype == "csv" else "left",
        numalign            = None if outputtype == "csv" else "rigth"
    )

    if outputfile:
        try:
            with open(outputfile, "w", encoding="utf-8") as out:
                out.write(tablestr)

            log.info(f"Resultado del proceso en: {outputfile}")

        except Exception as err:
            log.exception(str(_err))

    else:
        print("")
        print("Resultados:")
        print(tablestr)

def main():
    """Función Inicial"""

    print(TITLE)

    cmdparser = init_argparse()
    args = cmdparser.parse_args()

    log = Log(filename=args.logfile,
              loglevel=args.loglevel,
              quiet=args.quiet
    )

    log.info(f"Iniciando {NAME} - {DESCRIPTION} (v{VERSION})")

    # Lectura de archivo config
    #
    # determine if application is a script file or frozen exe
    application_path = None
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        # application_path = os.path.dirname(__file__)
        application_path = os.path.abspath(sys.argv[0])

    log.info(f"Carpeta de inicio {application_path}")

    try:
        cfg = Config('scrapper.cfg')

    except FileNotFoundError as _err:
        log.error(str(_err))
        sys.exit(-1)

    log.info(f"Cargando configuración: {cfg.cfgfile}")

    # Leemos las definiciones de los procesos
    #
    available_procs = []
    for section_name in cfg.config.sections():
        if "proc:" in section_name:
            available_procs.append((section_name.split(":")[1],
                                    cfg.config[section_name]["name"]))

    # Mostramos procesos disponibles
    #
    if args.show:
        show_procs(available_procs)
        sys.exit(0)

    # Intentamos ejecutar el proceso
    #
    if args.outputfile:
        workpath = os.path.dirname(os.path.abspath(args.outputfile))
        if workpath is None or workpath == "":
            workpath = tempfile.mkdtemp()
    else:
        workpath = tempfile.mkdtemp()

    datos = []
    if args.proceso is None:
        log.error("Debe especificar un proceso a ejecutar")
        sys.exit(-1)
    else:
        start_time = time.time()
        proceso = [p[0] for p in available_procs if p[0] == args.proceso][0]
        if proceso:

            datos = scrap(proceso,
                          cfg.config,
                          log,
                          args.inputparam,
                          args.inputfile,
                          workpath,
                          args.show_browser)

        else:
            # pylint: disable=line-too-long
            errormsg = f"No existe el proceso [{args.proceso}], verifique los procesos habilitados mediante scrapper -s"
            log.error(errormsg)
            sys.exit(-1)

    # Retornamos los resultados del proceso
    #
    n_rows = 0
    if datos:
        n_rows = len(datos) - 1
        if n_rows > 0:

            return_datos(log,
                        os.path.abspath(args.outputfile),
                        args.outputtype,
                        datos)

    elapsed_time = time.strftime('%H:%M:%S', time.gmtime(round(time.time() - start_time, 2)))
    log.info(f"Se salvaron {n_rows} filas en {elapsed_time}")
