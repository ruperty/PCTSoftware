set ENV=WebotsWrestler
set PORT=6670

set PYTHONPATH=%PYTHONPATH%;%USERPROFILE%\Versioning\PCTSoftware\Libraries\python\webots\controllers;C:\Program Files\Webots\lib\controller\python;%USERPROFILE%\Versioning\PCTSoftware\Libraries\python\pctlocal\tests\ga\pctobject




set CONFIG=WW01-09-RewardError-CurrentError-Mode03
%USERPROFILE%\AppData\Local\Programs\Python\Python39\python.exe %USERPROFILE%\Versioning\PCTSoftware\Libraries\python\pctlocal\tests\ga\pctobject\examples\evolve.py %ENV% %CONFIG% -p %PORT%

set CONFIG=WW01-10-RewardError-CurrentError-Mode03
%USERPROFILE%\AppData\Local\Programs\Python\Python39\python.exe %USERPROFILE%\Versioning\PCTSoftware\Libraries\python\pctlocal\tests\ga\pctobject\examples\evolve.py %ENV% %CONFIG% -p %PORT%


pause