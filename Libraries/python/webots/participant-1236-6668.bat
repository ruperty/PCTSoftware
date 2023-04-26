set PYTHONPATH=%PYTHONPATH%;%USERPROFILE%\Versioning\PCTSoftware\Libraries\python\webots\controllers;C:\Program Files\Webots\lib\controller\python

::echo %PYTHONPATH%

set WEBOTS_CONTROLLER_URL=ipc://1236

python controllers\participant\participant.py -p 6668

pause