#!/bin/bash
#Michael AI Docker Installation

echo "Doing Some Host Side Work for Michael to Work ..."

mkdir -p /home/$USER/.michael

python3 -m venv /home/$USER/michael/venv

cp host_files/* /home/$USER/.michael

source venv /home/$USER/michael/venv/bin/activate && pip install -r /home/$USER/.michael/host_requirements.txt

source venv /home/$USER/michael/venv/bin/activate && playwright install firefox

chmod +x /home/$USER/.michael/initial.sh

bash /home/$USER/.michael/initial.sh

mv ./modules/adb_call.sh /usr/local/bin/adb_call

echo "Installation Completed !!!,Michael is Ready..."
