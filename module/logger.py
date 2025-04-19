import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a formatter
formatter = logging.Formatter(
    "[%(asctime)s] [%(filename)s] [%(levelname)s]: %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S'
    )

# Create a file handler
file_handler = logging.FileHandler("../logfile.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)  # Set the file handler level
file_handler.setFormatter(formatter)  # Attach the formatter to the file handler

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Set the console handler level
console_handler.setFormatter(formatter)  # Attach the formatter to the console handler

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)