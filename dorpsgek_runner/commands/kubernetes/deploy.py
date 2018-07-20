from dorpsgek_runner import runner
from dorpsgek_runner.helpers.subprocess import run_command


@runner.register("kubernetes.deploy")
async def kubernetes_deploy(event, ws):
    namespace, _, deployment_name = event.data["name"].lower().partition("/")
    image_name = f"{event.data['name']}:{event.data['tag']}".lower()

    await run_command(f"kubectl --namespace={namespace} set image deployment/{deployment_name}"
                      f" {deployment_name}={image_name}")
