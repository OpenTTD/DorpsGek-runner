import logging
import os

from dorpsgek_runner import runner
from dorpsgek_runner.helpers.subprocess import run_command

log = logging.getLogger(__name__)


@runner.register("artifact.transfer")
async def artifact_transfer(event, ws):
    artifact_name = event.data["name"]
    artifact_size = event.data["size"]
    log.info("Receiving artifact '%s' (size: %d bytes)", event.data["name"], artifact_size)

    work_folder = f"{ws.tempdir.name}"
    artifact_folder = f"{work_folder}/{artifact_name}"
    artifact_tarball = f"{work_folder}/artifact/{artifact_name}.tar.gz"

    with open(artifact_tarball, "wb") as f:
        while artifact_size:
            data = await ws.receive_bytes()
            artifact_size -= len(data)

            f.write(data)

    os.mkdir(artifact_folder)
    await run_command(f"tar zxf {artifact_tarball} .", cwd=artifact_folder)


@runner.register("artifact.transfer_done")
async def artifact_transfer_done(event, ws):
    # No need to take any action here.
    # This is just for the server to sense we received the artifact.
    pass
