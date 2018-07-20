import os
import tempfile

from dorpsgek_runner import config
from dorpsgek_runner import runner


@runner.register("job.start")
async def job_start(event, ws):
    ws.tempdir = tempfile.TemporaryDirectory("", "runner.", config.WORKING_FOLDER)
    os.mkdir(f"{ws.tempdir.name}/artifact")


@runner.register("job.done")
async def job_done(event, ws):
    ws.tempdir.cleanup()
    ws.tempdir = None
