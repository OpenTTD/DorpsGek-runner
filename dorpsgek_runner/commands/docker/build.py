import logging

from dorpsgek_runner import runner
from dorpsgek_runner.helpers.subprocess import run_command

log = logging.getLogger(__name__)


@runner.register("docker.build")
async def docker_build(event, ws):
    source_folder = f"{ws.tempdir.name}/source"
    image_name = f"{event.data['name']}:{event.data['tag']}".lower()

    log.info("Building new image {image_name} ...")
    await run_command(f"docker build --pull -t {image_name} .", cwd=source_folder)
