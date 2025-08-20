import subprocess
import os

def run_script(script_name):
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    result = subprocess.run(['python', script_path], capture_output=True, text=True)
    print(f"Running {script_name}...")
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    if result.returncode != 0:
        print(f"Error: {script_name} exited with code {result.returncode}")
        exit(result.returncode)

if __name__ == "__main__":
    run_script("petdictgen.py")
    run_script("skilldictgen.py")
    run_script("specdictgen.py")
