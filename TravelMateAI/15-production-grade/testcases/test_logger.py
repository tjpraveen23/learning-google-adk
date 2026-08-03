import os
import sys
import uuid

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from travel_agent.logger import (
    get_logger,
    set_request_id,
)

logger = get_logger("test_logger")

request_id = str(uuid.uuid4())

set_request_id(request_id)

logger.info("Travel request received")
logger.info("WeatherAgent started")
logger.info("WeatherAgent completed")