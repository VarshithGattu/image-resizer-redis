# utils.py - Contains utility functions, primarily for logging

import logging
import os

def setup_logging(log_file='app.log', log_level=logging.INFO):
    """Sets up basic logging configuration."""
    
    # Ensure the log file directory exists
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    # Silence verbose logs from external libraries
    logging.getLogger('redis').setLevel(logging.WARNING)
    logging.getLogger('rq').setLevel(logging.WARNING)