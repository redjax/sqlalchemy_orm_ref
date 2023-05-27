from core.config import app_settings, logging_settings
from utils.logger import get_logger

log = get_logger(__name__, level=logging_settings.LOG_LEVEL)


if __name__ == "__main__":
    log.info("Starting app")
    
    log.debug(f"App settings: {app_settings}")
