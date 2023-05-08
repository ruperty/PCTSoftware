set ENV=WebotsWrestler
set CONFIG=WW01-05-RewardError-CurrentError-Mode01
set PORT=6668

set PYTHONPATH=%PYTHONPATH%;%USERPROFILE%\Versioning\PCTSoftware\Libraries\python\webots\controllers;C:\Program Files\Webots\lib\controller\python;%USERPROFILE%\Versioning\PCTSoftware\Libraries\python\pctlocal\tests\ga\pctobject


%USERPROFILE%\AppData\Local\Programs\Python\Python39\python.exe %USERPROFILE%\Versioning\PCTSoftware\Libraries\python\pctlocal\tests\ga\pctobject\examples\evolve.py %ENV% %CONFIG% -p %PORT%



pause