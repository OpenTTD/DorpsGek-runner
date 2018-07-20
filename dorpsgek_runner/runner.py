from collections import defaultdict


_registry = defaultdict(list)


class RunnerEventDoesntExist(Exception):
    """Thrown if the event given to process doesn't have any handlers."""


async def process_request(event, ws, wants_response=False):
    """
    Process a single request.
    """

    if not len(_registry[event.type]):
        raise RunnerEventDoesntExist(event.type)

    for func in _registry[event.type]:
        response = await func(event, ws)
        if wants_response:
            await ws.send_event("response", response)


def register(command):
    """Register an event for the runner."""

    def wrapped(func):
        _registry[command].append(func)
        return func
    return wrapped
