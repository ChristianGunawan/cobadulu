@echo off
REM MIT-License PYTHON LEXER and Parser (c) 2021, Coba Dulu. 13519075, 13519109, 13519199

REM mencatat jumlah argument (Argument Count)
SET argC=0
FOR %%x in (%*) DO SET /A argC+=1

REM jika argument == 1 maka proses file
IF %argC% == 1  (

    REM mengecek existensi file
    IF exist %1 (
        REM file ada
        @echo Lexing file %1%
        python src/lexer.py %1%
    ) ELSE (
        REM file tidak ada
        @echo file %1% tidak ada
    )

) ELSE (
    @echo invalid arguments.
)

exit /B 1