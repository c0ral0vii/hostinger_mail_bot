import logging
from logging.handlers import RotatingFileHandler
import pathlib


async def setup_logger(path: pathlib.Path, debug: bool = False):
    '''
    Инициализация логгера

    :return:
    '''

    logger = logging.getLogger('bot_logger')

    logger.setLevel(logging.DEBUG)

    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    if debug:
        debug_handler = logging.StreamHandler()
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(logging.Formatter(format))

        logger.addHandler(debug_handler)


    info_handler = RotatingFileHandler(f'{path}/info.log', maxBytes=5*1024*1024, backupCount=5, encoding='utf-8')
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(logging.Formatter(format))

    error_handler = RotatingFileHandler(f'{path}/error.log', maxBytes=5*1024*1024, backupCount=5, encoding='utf-8')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(format))


    logger.addHandler(info_handler)
    logger.addHandler(error_handler)

    return logger