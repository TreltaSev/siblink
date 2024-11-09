import os
import subprocess
import click
from pyucc import console
from siblink import Config, __git__
from pathlib import Path
import datetime


@click.command()
@Config.click_forward
@Config.load_predetermined
def init():
  """
  [init] Initializes a python project and installs 
  all required packages and virtual environments
  for siblink to work seamlessly.
  """
  # [Start of Time]
  tick = datetime.datetime.now()

  console.info("[init] Initializing...")

  # Check if venv exists, if not exists create venv with python -m venv venv
  if not Config.venv.exists():
    console.warn("[init] No Virtual Environment in current path, generating venv...")
    subprocess.run("python -m venv venv".split(" "), capture_output=True)
    console.success("[init] Virtual Environment created.")
    Config.gather_predetermined()

  # Install all modules in requirements.txt if its present
  if Path("./requirements.txt").exists():
    console.info("[init] requirements.txt file found, installing packages...")
    print(f"[output check] {Config} {Config.pip_exe}\n", f"{Config.pip_exe} install -r ./requirements.txt".split(" "))
    subprocess.run(f"{Config.pip_exe} install -r ./requirements.txt".split(" "), capture_output=True)
    console.success("[init] Installed Packages")

  console.info(f"[init] installing siblink in Virtual Environment")
  subprocess.run(f"{Config.pip_exe} install --upgrade --force-reinstall -I {__git__}".split(" "), capture_output=True)
  console.success(f"[init] Done! {round((datetime.datetime.now() - tick).total_seconds(), 2)}s")
  return
