#
# script to check current code against known solution files
#

for FN in ?? i4
do
    if [ "$FN" == "i4" ]
    then
        ../queens.py xxx > foo$$ 2>err$$
    else
        ../queens.py < $FN > foo$$ 2>err$$
    fi
    tail -1 err$$ >> foo$$
    cmp ../solutions/$FN foo$$
    if [ $? -eq 0 ]; then
        echo -n "$FN "
    else
        echo
        echo "***** failed check for case $FN *****"
        exit 1
    fi
done

rm foo$$ err$$
echo
echo "All tests passed"
