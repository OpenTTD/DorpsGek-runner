from dorpsgek_runner import runner


@runner.register("registered")
async def registered(event, ws):
    # Currently no action needed
    pass
