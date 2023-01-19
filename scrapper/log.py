import logging
import os

class Log:

    def __init__(self, outputpath, loglevel, quiet = True):

        logging.basicConfig(filename=os.path.join(outputpath, 'scrapper.log'),
                            level=getattr(logging, loglevel.upper(), None),
                            format='%(asctime)s|%(levelname)s|%(message)s',
                            datefmt='%Y/%m/%d %I:%M:%S',
                            filemode='w')
        self.quiet = quiet


    def info(self, msg):

        if not self.quiet:
            print(msg)

        logging.info(msg.replace("|", " "))

    def debug(self, msg):

        logging.debug(msg.replace("|", " "))

    def exception(self, msg):

        if not self.quiet:
            print(f"!!!Se ha producido una excepción al {msg}")

        logging.exception(msg.replace("|", " "))

    def error(self, msg):

        if not self.quiet:
            print(f"!!!Se ha producido un error al {msg}")

        logging.error(msg.replace("|", " "))

