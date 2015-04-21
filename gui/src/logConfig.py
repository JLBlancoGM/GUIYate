"""
Created on 15/04/15

AUTHOR: Jose Luis Blanco
PROJECT:  GUIYate 
CONTACT: blancogmoreno@gmail.com
VERSION: Log file config
SUMARY:  
"""


import logging
import os.path


def init_logger(output_dir):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create debug file handler and set level to debug
    handler = logging.FileHandler(os.path.join(output_dir, "guiyate.log"), "w")
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)