if [ "$#" -eq 1 ]
then
    if [ -f "$1" ]
    then
        echo lexing file "$1"
        python3 src/lexer.py "$1"
    else
        echo file "$1" tidak ada
    fi
else
    echo invalid arguments
fi
