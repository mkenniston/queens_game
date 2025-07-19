#
# script to generate solution files
#

for FN in ??
do
    ../queens.py < $FN > ../solutions/$FN
done
