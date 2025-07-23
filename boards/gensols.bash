#
# script to generate solution files
# Files 00-99 are from https://www.queens-game.com
#

for FN in ??
do
    ../queens.py < $FN > ../solutions/$FN
done
