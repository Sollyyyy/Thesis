import asyncio
import subprocess
import sys
import os
import json
from config import FLIGHT_API_KEY

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')


async def run_script(script, args):
    env = {**os.environ, 'FLIGHT_API_KEY': FLIGHT_API_KEY}
    try:
        process = await asyncio.create_subprocess_exec(
            sys.executable, script, *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=SCRIPTS_DIR,
            env=env
        )
        stdout, stderr = await process.communicate()
        if process.returncode == 0:
            return json.loads(stdout.decode())
        return {"success": False, "error": stderr.decode()}
    except Exception as e:
        return {"success": False, "error": str(e)}
