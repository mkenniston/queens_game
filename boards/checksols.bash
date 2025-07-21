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
        echo "\n***** $FN failed check *****"
    fi
done
rm foo$$
echo

