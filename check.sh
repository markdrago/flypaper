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

#only return 0 if both tests returned 0
exit $(( $test_result || $pep8_result))

