#!/bin/bash

pip install twine wheel

python setup.py sdist bdist_wheel
python -m twine upload dist/*