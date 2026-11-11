import importlib.metadata as metadata
import re
import subprocess
import sys
import tempfile
import venv
from pathlib import Path

# pip INSTALLS packages from PyPI (the Python Package Index). You run it in a terminal:
#
#   python -m pip install requests            install the newest version
#   python -m pip install "requests==2.31.0"  an exact version
#   python -m pip install "requests>=2.31,<3" a range
#   python -m pip install -U requests         upgrade
#   python -m pip uninstall requests
#   python -m pip list                        everything installed
#   python -m pip show requests               details of one package
#   python -m pip freeze > requirements.txt   write the exact versions you use
#   python -m pip install -r requirements.txt install them all again
#   python -m pip install -e .                install YOUR project in "editable" mode
#   python -m pip check                       look for broken dependencies
#
# Always write "python -m pip" (not just "pip"): it is sure to use the SAME Python you run.

# 1. Which Python am I running?
print(sys.version_info >= (3, 10))                      # True
print(isinstance(sys.prefix != sys.base_prefix, bool))  # True    (the value is True inside a venv)

# 2. Installed packages can be inspected from Python
try:
    print(isinstance(metadata.version("pip"), str))     # True
except metadata.PackageNotFoundError:
    print("pip is not installed in this Python")

# 3. A VIRTUAL ENVIRONMENT is a private folder of packages for ONE project.
#    Create one from Python (without pip inside, so it works offline):
with tempfile.TemporaryDirectory() as tmp:
    env_dir = Path(tmp) / "demo-env"
    venv.create(env_dir, with_pip=False)
    scripts = "Scripts" if sys.platform == "win32" else "bin"
    config = (env_dir / "pyvenv.cfg").read_text(encoding="utf-8")
    print((env_dir / scripts).is_dir(), "include-system-site-packages = false" in config)
    # True True

# 4. Run pip as a program from Python
result = subprocess.run([sys.executable, "-m", "pip", "--version"], capture_output=True, text=True)
print(result.returncode == 0, result.stdout.startswith("pip "))     # True True

# 5. Reading a requirements.txt
REQUIREMENTS = """\
# web
requests>=2.31,<3
numpy==1.26.4

pandas ; python_version >= "3.9"
-e .
"""

names, pinned = [], {}
for line in REQUIREMENTS.splitlines():
    line = line.split("#")[0].strip()
    if not line or line.startswith("-"):        # blank lines and options such as -e
        continue
    names.append(re.match(r"[A-Za-z0-9_.-]+", line).group())
    if "==" in line:
        name, version = line.split("==")
        pinned[name] = version
print(names, pinned)                            # ['requests', 'numpy', 'pandas'] {'numpy': '1.26.4'}

# THE ROUTINE FOR EVERY PROJECT (VS Code terminal)
#   python -m venv .venv                         create the environment in the folder .venv
#   .venv\Scripts\activate                       Windows (PowerShell: .venv\Scripts\Activate.ps1)
#   source .venv/bin/activate                    macOS / Linux
#   python -m pip install -r requirements.txt
#   deactivate                                   leave the environment
# In VS Code choose the interpreter: Ctrl+Shift+P, "Python: Select Interpreter", pick .venv.
# Add .venv/ to .gitignore. Never commit the environment, only requirements.txt.
#
# VERSION SPECIFIERS      ==1.2.3 exact   >=1.2 at least   <3 below   !=1.5 not   ~=1.4.2 compatible
# WHEEL (.whl)            a ready-to-install package. SDIST (.tar.gz) is source that must be built.
# pyproject.toml          the modern project file: name, version, dependencies, build system.
#       [project]
#       name = "mytool"
#       version = "0.1.0"
#       dependencies = ["requests>=2.31"]
#   Build with:  python -m pip install build ; python -m build      Upload with: twine
# OTHER TOOLS             pipx (install command-line apps), uv (a very fast pip + venv), conda
# SAFETY                  check the exact package name (typosquatting), pin versions, read what you
#                         install, use "pip-audit" to look for known vulnerabilities.