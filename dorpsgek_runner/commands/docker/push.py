import logging

from dorpsgek_runner import runner
from dorpsgek_runner.helpers.subprocess import run_command

log = logging.getLogger(__name__)


@runner.register("docker.push")
async def docker_push(event, ws):
    image_name = f"{event.data['name']}:{event.data['tag']}".lower()

    log.info("Pushing new image {image_name} to repository ...")
    await run_command(f"docker push {image_name}")
