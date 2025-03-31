{ pkgs ? import <nixpkgs> { } }:

let
  python = pkgs.python312;
  pythonPackages = python.pkgs;
  lib-path = with pkgs; lib.makeLibraryPath [
    libffi
    openssl
    stdenv.cc.cc
  ];

in

pkgs.mkShell {

  packages = [
    pythonPackages.pip
    pythonPackages.setuptools
    pythonPackages.wheel
    pythonPackages.virtualenv
    pythonPackages.cython
    pythonPackages.PyGithub
  ];

  buildInputs = [
    # Java
    pkgs.jre # Java Runtime Environment

    # C++ development tools
    pkgs.gcc # GNU Compiler Collection

    python
  ];


  hardeningDisable = [ "fortify" ];

  shellHook = ''
    echo "Python $(python --version) installed"

    export "LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${lib-path}"
    echo "Set code-insiders alias"
    alias codeinsiders="/mnt/c/Users/machajai/AppData/Local/Programs/Microsoft\ VS\ Code\ Insiders/bin/code-insiders"
    # Create and activate Python virtual environment if it doesn't exist
    VENV_DIR=".venv"
    if [ ! -d "$VENV_DIR" ]; then
      echo "Creating Python virtual environment in $VENV_DIR..."
      python -m venv "$VENV_DIR" --copies
    fi

    # Activate the virtual environment
    source "$VENV_DIR/bin/activate"
    echo "Python virtual environment activated: $(which python)"

    # Upgrade pip to latest version
    pip install --upgrade pip

    # Install package in development mode using setup.py if it exists
    if [ -f setup.py ]; then
      echo "Installing package in development mode using setup.py..."
      pip install -e .
    elif [ -f requirements.txt ]; then
      echo "No setup.py found. Installing dependencies from requirements.txt instead..."
      pip install -r requirements.txt --no-binary aiohttp
    else
      echo "Neither setup.py nor requirements.txt found. Skipping dependencies installation."
    fi
  '';

  postShellHook = ''
    ln -sf ${python.sitePackages}/* ./.venv/lib/python3.12/site-packages
  '';
}

