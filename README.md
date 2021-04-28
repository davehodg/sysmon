# sysmon
Simple flask app to see the stats of a remote machine.

It's a de-classed version of
https://hackersandslackers.com/automate-ssh-scp-python-paramiko/

I'd strongly recommend using paython3.

If I have to use it in anger, I'll re-class it. Also, keep variables
in a configfile. Or secrets in github if I set an action.

Set:

FLASK_ENV=development
FLASK_APP=sysmon.py

Then do:

flask run

