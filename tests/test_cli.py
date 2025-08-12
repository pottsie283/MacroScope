import subprocess
import sys
import os

def test_cli_json():
    test_file = os.path.join(os.path.dirname(__file__), "../macroscope/__init__.py")
    result = subprocess.run([sys.executable, "../scripts/cli.py", "analyze", test_file, "--format", "json"], capture_output=True, text=True)
    assert result.returncode == 0
    assert 'SHA256:' in result.stdout
    assert 'findings' in result.stdout or 'Findings' in result.stdout

def test_cli_text():
    test_file = os.path.join(os.path.dirname(__file__), "../macroscope/__init__.py")
    result = subprocess.run([sys.executable, "../scripts/cli.py", "analyze", test_file, "--format", "text"], capture_output=True, text=True)
    assert result.returncode == 0
    assert 'SHA256:' in result.stdout
    assert 'Risk Score:' in result.stdout
