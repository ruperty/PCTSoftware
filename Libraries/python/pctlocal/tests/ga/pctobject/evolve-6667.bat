set PYTHONPATH=%PYTHONPATH%;%USERPROFILE%\Versioning\PCTSoftware\Libraries\python\webots\controllers;C:\Program Files\Webots\lib\controller\python;%USERPROFILE%\Versioning\PCTSoftware\Libraries\python\pctlocal\tests\ga\pctobject

set ENV=WebotsWrestler
set PORT=6667

set CONFIG=WW01-03-RewardError-CurrentError-Mode01

%USERPROFILE%\AppData\Local\Programs\Python\Python39\python.exe %USERPROFILE%\Versioning\PCTSoftware\Libraries\python\pctlocal\tests\ga\pctobject\examples\evolve.py %ENV% %CONFIG% -p %PORT%

set CONFIG=WW01-04-RewardError-CurrentError-Mode01

%USERPROFILE%\AppData\Local\Programs\Python\Python39\python.exe %USERPROFILE%\Versioning\PCTSoftware\Libraries\python\pctlocal\tests\ga\pctobject\examples\evolve.py %ENV% %CONFIG% -p %PORT%



::pause