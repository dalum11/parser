import requests
from parser.config import settings
from parser.utils.logger import get_logger

logger = get_logger(__name__)

def fetch(url: str) -> requests.Response:
    logger.debug("GET %s (timeout=%s)", url, settings.request_timeout)
    response = requests.get(
        url,
        timeout=settings.request_timeout,
        headers={"User-Agent": settings.user_agent}
    )
    logger.info("GET %s -> %s: %s", url, response.status_code, response.reason)
    return response