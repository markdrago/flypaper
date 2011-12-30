#!/bin/sh

#run unit tests
cd src
python -m unittest discover
test_result=$?
cd ..

#check pep8 style guidelines
which pep8 > /dev/null
if [ $? != 0 ]; then
    echo 'install pep8: pip install pep8'
else
    find -name '*.py' | xargs pep8
    pep8_result=$?
fi

if [ $test_result != 0 -o $pep8_result != 0 ]; then
    exit 1
fi

exit 0
