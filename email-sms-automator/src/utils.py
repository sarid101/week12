# email-sms-automator/src/utils.py
import logging
import os
from dotenv import load_dotenv

# Load environment variables from the .env file in the project root
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(_PROJECT_ROOT, '.env'))

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def setup_logging(name, level=logging.INFO):
    """Sets up a logger for specific modules."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:  # Prevent adding multiple handlers if called multiple times
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.propagate = False  # Avoid printing every message twice
    return logger


def get_env_variable(var_name):
    """Retrieves an environment variable, raising an error if not found."""
    value = os.getenv(var_name)
    if value is None or value.strip() == "":
        raise ValueError(f"Environment variable '{var_name}' not set. "
                         f"Please check your .env file or environment settings.")
    return value.strip()


def ensure_directory_exists(path):
    """Ensures that a directory exists, creating it if necessary."""
    if not path:
        return
    try:
        os.makedirs(path, exist_ok=True)
        logging.info(f"Directory ensured: {path}")
    except OSError as e:
        logging.error(f"Error creating directory {path}: {e}")
        raise
