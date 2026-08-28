"""Fixture: a shell-script-style CLI output consumer."""
import subprocess

proc = subprocess.run(["deployctl", "--version"], capture_output=True, text=True)
version_line = proc.stdout.strip().splitlines()[0]
print("deployctl version:", version_line)
