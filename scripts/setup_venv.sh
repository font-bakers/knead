#/bin/bash

PYTHON=$1
VENV_PATH=$2

$PYTHON -m venv $VENV_PATH
source $VENV_PATH/bin/activate
pip install --upgrade pip

for line in $(grep -v \# requirements.txt)
do
   pip install $line
done

deactivate
