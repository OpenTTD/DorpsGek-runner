import asyncio
import shlex


class CommandError(Exception):
    """Thrown if the exit code of the command was non-zero."""


async def run_command(command, cwd=None):
    process = await asyncio.create_subprocess_exec(
        *shlex.split(command),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=cwd,
    )

    return_code = await process.wait()
    if return_code != 0:
        stderr = []
        while True:
            line = await process.stderr.readline()
            if not line:
                break
            stderr.append(line.decode())

        raise CommandError(return_code, command, "\n".join(stderr))
