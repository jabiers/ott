for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"

set "datestamp=%MM%%DD%" & set "timestamp=%HH%%Min%%Sec%"
set "fullstamp=%MM%-%DD%_%HH%%Min%%Sec%"
SET BAT_PATH=%~dp0
echo %BAT_PATH%
mkdir bin\%fullstamp%\source
copy %BAT_PATH%\*.pyw %BAT_PATH%\bin\%fullstamp%\source\
PyInstaller build.spec --distpath bin\%fullstamp% --add-data "jabiott-firebase-adminsdk-w0rig-5b46a13752.json;," --icon=./ottv.ico --add-data "ottv.ico;."
