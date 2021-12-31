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
export BLACK_STATUS=$?
if [ $BLACK_STATUS -ne 0 ]; then
    echo "💥💥 Please run black on this source to reformat and resubmit 💥💥 "
fi

pylint $SOURCES
export PYLINT_STATUS=$?
if [ $PYLINT_STATUS -ne 0 ]; then
    echo "💥💥 Please fix the above pylint errors and resubmit 💥💥 "
fi

flake8 --max-line-length=100 $SOURCES
export FLAKE8_STATUS=$?
if [ $PYLINT_STATUS -ne 0 ]; then
    echo "💥💥 Please fix the above flake8 errors and resubmit 💥💥 "
fi

python3 -m unittest discover -s src/tests -t src
export TEST_STATUS=$?
if [ $TEST_STATUS -ne 0 ]; then
    echo "💥💥 Please fix the above test failures and resubmit 💥💥 "
fi

if [ "$1" = "run" ]; then python3 src/scheduling.py; fi

exit $(($BLACK_STATUS + $PYLINT_STATUS + $FLAKE8_STATUS + $TEST_STATUS))
