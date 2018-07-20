import logging
import time

from dorpsgek_runner import runner, config

log = logging.getLogger(__name__)


@runner.register("welcome")
async def welcome(event, ws):
    await ws.send_event("register", {"environment": config.ENVIRONMENT})
    await ws.send_event("ping", {"time": time.time()})
    log.info("Runner registered in environment '%s'", config.ENVIRONMENT)
