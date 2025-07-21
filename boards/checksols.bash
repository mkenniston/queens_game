#
# script to check current code against known solution files
#

for FN in ??
do
    ../queens.py < $FN > foo$$
    cmp ../solutions/$FN foo$$
    if [ $? -eq 0 ]; then
        echo -n "$FN "
    else
        echo
        echo "***** failed check for case $FN *****"
        exit 1
    fi
done
rm foo$$
echo
echo "All tests passed"
