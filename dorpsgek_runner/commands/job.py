import logging
import os
import tempfile

from dorpsgek_runner import config
from dorpsgek_runner import runner

log = logging.getLogger(__name__)


@runner.register("job.start")
async def job_start(event, ws):
    log.info("Starting with a new job")

    ws.tempdir = tempfile.TemporaryDirectory("", "runner.", config.WORKING_FOLDER)
    os.mkdir(f"{ws.tempdir.name}/artifact")


@runner.register("job.done")
async def job_done(event, ws):
    ws.tempdir.cleanup()
    ws.tempdir = None

    log.info("All done with the requested job")
