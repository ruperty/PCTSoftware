set PYTHONPATH=%PYTHONPATH%;%USERPROFILE%\Versioning\PCTSoftware\Libraries\python\webots\controllers;C:\Program Files\Webots\lib\controller\python

::echo %PYTHONPATH%

set WEBOTS_CONTROLLER_URL=ipc://1235

python controllers\participant\participant.py -p 6667

pause