# devops_task

Fedora-Workstation-Live-i386-29-1.2.iso
---------------------------------------
passwd: nezn8m0_0

sudo yum -y upgrade

requests
--------

pip-3 install requests

Running
-------

chmod u+x ./producer.extension.sh ./consumer.py

# Terminál 1
while true; do ./producer.extension.sh 2014.06 `date '+%Y-%m-%d'` `date '+%H:%M:%S'`; sleep 11; done

# Terminál 2
python3 ./consumer.py

