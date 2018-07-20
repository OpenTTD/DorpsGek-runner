import aiohttp
import asyncio
import importlib
import logging

from aiohttp import WSMsgType

from dorpsgek_runner import config, runner
from dorpsgek_runner.load_config import load_config
from dorpsgek_runner.runner import RunnerEventDoesntExist

log = logging.getLogger(__name__)
# These commands should always be loaded to have a functional runner.
# They do not contain any code that can be executed.
# Only to register and get things started.
COMMANDS_ALWAYS_LOAD = ["job", "pong", "registered", "welcome"]


class RunnerEvent:
    """Event that comes from a runner."""
    def __init__(self, type, data=None):
        self.type = type
        self.data = data


async def ws_send_event(self, event, data=None):
    """Easy helper function to send an event over the wire."""
    payload = {
        "type": event,
    }
    if data:
        payload["data"] = data

    await self.send_json(payload)
aiohttp.client_ws.ClientWebSocketResponse.send_event = ws_send_event


async def run(session, address):
    log.info("Connecting to '%s' ...", address)
    try:
        ws = await session.ws_connect(address)
    except aiohttp.client_exceptions.ClientConnectorError:
        log.error("Failed to connect to '%s'", address)
        return

    log.info("Connection established; waiting for welcome message")

    async for msg in ws:
        if msg.type == WSMsgType.CLOSED:
            break
        elif msg.type == WSMsgType.TEXT:
            raw = msg.json()
            if raw["type"] == "request":
                wants_response = True
                event = RunnerEvent(raw["data"]["type"], raw["data"].get("data"))
            else:
                wants_response = False
                event = RunnerEvent(raw["type"], raw.get("data"))

            try:
                await runner.process_request(event, ws, wants_response)
            except RunnerEventDoesntExist as err:
                await ws.send_event("error", {"command_does_not_exist": err.args[0]})
        else:
            log.error(f"Unexpected message type {msg.type}")
            break


async def run_forever(address):
    while True:
        session = aiohttp.ClientSession()
        try:
            await run(session, address)
            log.info("Lost connection to server")
        except Exception:
            log.exception("Unexpected error")
        finally:
            await session.close()

        # Make sure we don't hammer the server on errors
        log.info("Waiting 5 seconds before retrying to connect ...")
        await asyncio.sleep(5)


def main():
    logging.basicConfig(level=logging.INFO)
    load_config()

    for command in config.COMMANDS.split() + COMMANDS_ALWAYS_LOAD:
        importlib.import_module(f"dorpsgek_runner.commands.{command}")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_forever(config.DORPSGEK_ADDRESS))


if __name__ == "__main__":
    main()
