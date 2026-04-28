import subprocess
import sys
import os
import json
from config import FLIGHT_API_KEY

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')


def run_script(script, args):
    env = {**os.environ, 'FLIGHT_API_KEY': FLIGHT_API_KEY}
    try:
        result = subprocess.run(
            [sys.executable, script] + args,
            capture_output=True,
            text=True,
            cwd=SCRIPTS_DIR,
            env=env
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        return {"success": False, "error": result.stderr}
    except Exception as e:
        return {"success": False, "error": str(e)}
