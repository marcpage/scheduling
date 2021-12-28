#!bash

export OS_TYPE=`uname -s`
if [ "$OS_TYPE" = "Darwin" ]; then
    export VENV_DIR=$HOME/Library/Caches/venv/scheduling;
else
    export VENV_DIR=$HOME/.venv/scheduling;
fi

echo Creating Python venv: $VENV_DIR
mkdir -p $VENV_DIR
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate

pip3 install -qr Requirements.txt

if [ "$1" = "" ]; then export CHECK=--check; fi

black $CHECK src/*.py
pylint src/*.py
flake8 --max-line-length=100 src/*.py

if [ "$1" = "run" ]; then python3 src/scheduling.py; fi
