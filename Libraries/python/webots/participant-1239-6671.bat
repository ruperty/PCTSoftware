set PYTHONPATH=%PYTHONPATH%;%USERPROFILE%\Versioning\PCTSoftware\Libraries\python\webots\controllers;C:\Program Files\Webots\lib\controller\python

set WP=1238
set PORT=6670

set WEBOTS_CONTROLLER_URL=ipc://%WP%

python controllers\participant\participant.py -p %PORT% -wp %WP%

pause