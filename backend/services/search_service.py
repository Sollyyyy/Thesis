import subprocess
import sys
import os
import json

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')


def run_script(script, args):
    try:
        result = subprocess.run(
            [sys.executable, script] + args,
            capture_output=True,
            text=True,
            cwd=SCRIPTS_DIR
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        return {"success": False, "error": result.stderr}
    except Exception as e:
        return {"success": False, "error": str(e)}
