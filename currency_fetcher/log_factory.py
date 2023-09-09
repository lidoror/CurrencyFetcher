import logging


class LoggerFactory:

    def __init__(self, name='logger', level=logging.INFO, log_file=None,
                 encoding='utf-8', time_format='%d/%m/%Y %I:%M:%S %p'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        formatter = logging.Formatter('%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d [%(filename)s])',
                                      datefmt=time_format
                                      )

        if log_file:
            file_handler = logging.FileHandler(log_file, encoding=encoding)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger


logger = LoggerFactory().get_logger()
