#!bash

#GITHUB_WORKFLOW=CI

if [ "$GITHUB_WORKFLOW" = "CI" ]; then
    export LOG_ECHO=echo
    export ERROR_PREFIX="##[error]"
else
    export LOG_ECHO=true
fi

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
$LOG_ECHO "##[group] Running black python source validation"
$LOG_ECHO "##[command]black $CHECK $SOURCES"
black $CHECK $SOURCES
export BLACK_STATUS=$?
$LOG_ECHO "##[endgroup]"
if [ $BLACK_STATUS -ne 0 ]; then
    echo $ERROR_PREFIX"💥💥 Please run black on this source to reformat and resubmit 💥💥 "
else
    echo "✅ black verification successful"
fi

$LOG_ECHO "##[group] Running pylint python source validation"
$LOG_ECHO "##[command]pylint $SOURCES"
pylint $SOURCES
export PYLINT_STATUS=$?
$LOG_ECHO "##[endgroup]"
if [ $PYLINT_STATUS -ne 0 ]; then
    echo $ERROR_PREFIX"💥💥 Please fix the above pylint errors and resubmit 💥💥 "
else
    echo "✅ pylint verification successful"
fi

$LOG_ECHO "##[group] Running flake8 python source validation"
$LOG_ECHO "##[command]flake8 --max-line-length=100 $SOURCES"
flake8 --max-line-length=100 $SOURCES
export FLAKE8_STATUS=$?
$LOG_ECHO "##[endgroup]"
if [ $FLAKE8_STATUS -ne 0 ]; then
    echo $ERROR_PREFIX"💥💥 Please fix the above flake8 errors and resubmit 💥💥 "
else
    echo "✅ flake8 verification successful"
fi

$LOG_ECHO "##[group] Running python unit tests"
$LOG_ECHO "##[command]python3 -m unittest discover -s src/tests -t src"
python3 -m unittest discover -s src/tests -t src 2>&1 | sed "/SAWarning:/s/^/##[warning]/"
export TEST_STATUS=$?
$LOG_ECHO "##[endgroup]"
if [ $TEST_STATUS -ne 0 ]; then
    echo $ERROR_PREFIX"💥💥 Please fix the above test failures and resubmit 💥💥 "
else
    echo "✅ unit tests passed"
fi

if [ "$1" = "run" ]; then python3 src/scheduling.py --test; fi

exit $(($BLACK_STATUS + $PYLINT_STATUS + $FLAKE8_STATUS + $TEST_STATUS))
