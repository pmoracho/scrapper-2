"""Manejo de Log
"""
import logging

class Log:
    """Clase para el manejo de una auditoría ("Log") del proceso
    """

    def __init__(self, filename, loglevel, quiet = True):

        logging.basicConfig(filename=filename,
                            level=getattr(logging, loglevel.upper(), None),
                            format='%(asctime)s|%(levelname)s|%(message)s',
                            datefmt='%Y/%m/%d %I:%M:%S',
                            filemode='w')
        self.quiet = quiet


    def info(self, msg):
        """Log informativo"""
        if not self.quiet:
            print(msg)

        logging.info(msg.replace("|", " "))

    def info_internal(self, msg):
        """Log nivel info interna"""
        logging.info(msg.replace("|", " "))

    def debug(self, msg):
        """Log nivel debug"""
        logging.debug(msg.replace("|", " "))

    def exception(self, msg):
        """Log nivel excption"""
        if not self.quiet:
            print(f"!!!Se ha producido una excepción: {msg}")

        logging.exception(msg.replace("|", " "))

    def error(self, msg):
        """Log nivel error"""
        if not self.quiet:
            print(f"!!!Se ha producido un error {msg}")

        logging.error(msg.replace("|", " "))

