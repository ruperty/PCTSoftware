set ENV=WebotsWrestler
set CONFIG=WW01-08-RewardError-CurrentError-Mode02
set PORT=6667

set PYTHONPATH=%PYTHONPATH%;%USERPROFILE%\Versioning\PCTSoftware\Libraries\python\webots\controllers;C:\Program Files\Webots\lib\controller\python;%USERPROFILE%\Versioning\PCTSoftware\Libraries\python\pctlocal\tests\ga\pctobject


%USERPROFILE%\AppData\Local\Programs\Python\Python39\python.exe %USERPROFILE%\Versioning\PCTSoftware\Libraries\python\pctlocal\tests\ga\pctobject\examples\evolve.py %ENV% %CONFIG% -p %PORT%

python examples\evolve.py WebotsWrestler WW01-08-RewardError-CurrentError-Mode02 -p 6667






pause