#
# script to generate solution files
# Files 00-99 are from https://www.queens-game.com
#

for FN in ?? i4
do
    SOLN="../solutions/$FN"
    if [ "$FN" == "i4" ]
    then
        ../queens.py xxx > $SOLN 2>err$$
    else
        ../queens.py < $FN > $SOLN 2>err$$
    fi
    tail -1 err$$ >> $SOLN
done

rm err$$

