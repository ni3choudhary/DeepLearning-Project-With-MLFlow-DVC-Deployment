import os
import sys
import logging
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Get the logger level from the environment variable, defaulting to INFO if not specified
log_level = os.getenv("LOG_LEVEL", "INFO")

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

log_filepath = os.path.join(log_dir,"project_logs.log")

logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

logging.basicConfig(
    level= log_level,
    format= logging_str,

    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("DLProjectLogger")