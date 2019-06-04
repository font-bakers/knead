#/bin/bash
# Sets up Python virtual environment for development.

PYTHON=$1
VENV_PATH=$2

$PYTHON -m venv $VENV_PATH
source $VENV_PATH/bin/activate
pip install --upgrade pip

grep -v \# requirements-dev.txt | while read line
do
   echo $line
   pip install $line
done

deactivate
