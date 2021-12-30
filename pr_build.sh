#!bash

export OS_TYPE=`uname -s`
if [ "$OS_TYPE" = "Darwin" ]; then
    export VENV_DIR=$HOME/Library/Caches/venv/scheduling;
else
    export VENV_DIR=$HOME/.venv/scheduling;
fi

mkdir -p $VENV_DIR
python3 -m venv $VENV_DIR
. $VENV_DIR/bin/activate

pip3 install -qr Requirements.txt

if [ "$1" = "" ]; then export CHECK=--check; fi

export SOURCES="src/*.py"

black $CHECK $SOURCES
pylint $SOURCES
flake8 --max-line-length=100 $SOURCES

python3 -m unittest discover -s src/tests -t src

if [ "$1" = "run" ]; then python3 src/scheduling.py; fi
