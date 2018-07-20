from dorpsgek_runner import runner
from dorpsgek_runner.helpers.subprocess import run_command


@runner.register("docker.push")
async def docker_push(event, ws):
    image_name = f"{event.data['name']}:{event.data['tag']}".lower()

    await run_command(f"docker push {image_name}")
